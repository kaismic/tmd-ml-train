import os
import pandas as pd
from model_config import ModelConfig
import utils
from tqdm import tqdm
from skl2onnx import convert_sklearn
from skl2onnx.helpers.onnx_helper import save_onnx_model
from skl2onnx.common.data_types import FloatTensorType

class Train:
    config: ModelConfig
    df: pd.DataFrame

    def __init__(self) -> None:
        self.config = ModelConfig.from_yaml()

    def create_dataframe(self) -> None:
        """
        Create a DataFrame by reading all transformed CSV files and concatenating them together.
        - Each row in the resulting DataFrame corresponds to a window of sensor data.
        - The DataFrame will have a 'transport_mode' column indicating the transport mode for each window, derived from the file name.
        """

        input_files = list(self.config.transformed_data_path.rglob("*.csv"))
        print(f"Total files to read: {len(input_files)}")

        result_df = pd.DataFrame()
        for file in input_files:
            df = pd.read_csv(file)
            df['transport_mode'] = self.config.transport_modes[utils.get_transport_mode_from_path(file)]
            result_df = pd.concat([result_df, df], ignore_index=True)

        print(f"DataFrame shape before dropping rows with NaN: {result_df.shape}")
        print(f"\n{result_df.head()}")

        result_df = result_df.dropna()

        print(f"Final DataFrame shape: {result_df.shape}")
        print(f"\n{result_df.head()}")

        self.df = result_df


    def create_model(self, classifier, n_features):
        """Convert a fitted sklearn classifier to ONNX and write it to DIR_RESULTS."""
        initial_type = [('float_input', FloatTensorType([None, n_features]))]
        return convert_sklearn(classifier, initial_types=initial_type)

    def train_and_save_model(self) -> None:
        """
        """

        self.create_dataframe()

        os.makedirs(self.config.models_path, exist_ok=True)

        from sklearn.ensemble import RandomForestClassifier
        from sklearn.neural_network import MLPClassifier
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.svm import SVC
        from sklearn import tree

        x = self.df.drop(columns=['transport_mode'])
        y = self.df['transport_mode']

        algs = ['random_forest', 'decision_tree', 'knn', 'svm', 'neural_network']

        iter = tqdm(algs)
        for alg in algs:
            print(iter)
            match alg:
                case 'random_forest':
                    classifier = RandomForestClassifier(random_state=296737)
                case 'decision_tree':
                    classifier = tree.DecisionTreeClassifier()
                case 'knn':
                    classifier = KNeighborsClassifier()
                case 'svm':
                    classifier = SVC()
                case 'neural_network':
                    classifier = MLPClassifier()
                case _:
                    print("Unknown algorithm: ", alg)
                    return
            classifier.fit(x, y)
            model = self.create_model(classifier, len(x.columns))
            out_path = os.path.join(self.config.models_path, alg + '.onnx')
            save_onnx_model(model, out_path)
            print(f"Model trained and saved to {out_path}")
            iter.update()

        print("All training and models generation complete.")

if __name__ == "__main__":
    t = Train()
    t.train_and_save_model()