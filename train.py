import os
import pandas as pd
import constants
import utils
from skl2onnx import convert_sklearn
from skl2onnx.helpers.onnx_helper import save_onnx_model
from skl2onnx.common.data_types import FloatTensorType

def create_dataframe() -> pd.DataFrame:
    """
    Create a DataFrame by reading all transformed CSV files and concatenating them together.
     - Each row in the resulting DataFrame corresponds to a window of sensor data.
     - The DataFrame will have a 'transport_mode' column indicating the transport mode for each window, derived from the file name.
    """

    input_files = list(constants.TRANSFORMED_DATA_PATH.rglob("*.csv"))
    print(f"Total files to read: {len(input_files)}")

    result_df = pd.DataFrame()
    for file in input_files:
        df = pd.read_csv(file)
        df['transport_mode'] = constants.TRANSPORT_MODES[utils.get_transport_mode_from_path(file)]
        result_df = pd.concat([result_df, df], ignore_index=True)

    print(f"Final DataFrame shape: {result_df.shape}")
    print(f"Sample of DataFrame:\n{result_df.head()}")
    return result_df


def create_model(classifier, n_features):
    """Convert a fitted sklearn classifier to ONNX and write it to DIR_RESULTS."""
    initial_type = [('float_input', FloatTensorType([None, n_features]))]
    return convert_sklearn(classifier, initial_types=initial_type)


def train_and_save_model(df: pd.DataFrame) -> None:
    """
    """

    x = df.drop(columns=['transport_mode'])
    y = df['transport_mode']

    from sklearn.ensemble import RandomForestClassifier
    classifier = RandomForestClassifier(n_estimators=100, random_state=296737)
    classifier.fit(x, y)

    # Save the trained model in ONNX format
    model = create_model(classifier, len(x.columns))

    out_path = os.path.join(constants.MODELS_PATH, 'random_forest.onnx')
    save_onnx_model(model, out_path)

    print(f"Model trained and saved to {out_path}")


if __name__ == "__main__":
    df = create_dataframe()
    train_and_save_model(df)