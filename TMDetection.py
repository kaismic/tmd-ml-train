from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

from TMDataset import TMDataset
import const


class TMDetection:
    dataset = TMDataset()
    classes = []
    classes2string = {}
    classes2number = {}

    def __init__(self):
        if not const.HAVE_DT:
            self.dataset.create_balanced_dataset(const.SINTETIC_LEARNING)
        classes_dataset = self.dataset.get_dataset['target'].values
        print(classes_dataset)
        for i, c in enumerate(sorted(set(classes_dataset))):
            self.classes2string[i] = c
            self.classes2number[c] = i
            self.classes.append(c)

    def __get_full_dataset_for_classification(self):
        """Load the full balanced dataset and return features/classes arrays.
        Used by the create_*_model methods which train on all available data."""

        full_df = self.dataset.get_dataset
        print("CLASSIFICATION BASED ON THESE SENSORS: ", const.PROTOTYPE_SENSOR_FEATURES)
        for col in const.PROTOTYPE_SENSOR_FEATURES:
            col_mean = full_df[col].mean()
            na_count = full_df[col].isna().sum()
            print(f"{col}: {na_count} NaN values, mean={col_mean}")
            full_df[col] = full_df[col].fillna(col_mean)
        all_features = full_df[const.PROTOTYPE_SENSOR_FEATURES].values.astype(np.float32)
        all_classes = [self.classes2number[c] for c in full_df['target'].values]
        return all_features, all_classes
 

    def __save_onnx(self, classifier, n_features, model_name):
        """Convert a fitted sklearn classifier to ONNX and write it to DIR_RESULTS."""
        initial_type = [('float_input', FloatTensorType([None, n_features]))]
        onnx_model = convert_sklearn(classifier, initial_types=initial_type)
        models_dir = "models"
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        out_path = os.path.join(models_dir, model_name + '.onnx')
        with open(out_path, 'wb') as f:
            f.write(onnx_model.SerializeToString())
        print("ONNX model saved to: " + out_path)

    # Train a Decision Tree on the full dataset and export as .onnx
    def create_decision_tree_model(self):
        print("CREATING DECISION TREE ONNX MODEL.....")
        print("CLASSIFICATION BASED ON THESE SENSORS: ", const.PROTOTYPE_SENSORS)
        all_features, all_classes = self.__get_full_dataset_for_classification()
        print("NUMBER OF FEATURES: ", len(all_features))
        classifier = tree.DecisionTreeClassifier()
        classifier.fit(all_features, all_classes)
        self.__save_onnx(classifier, len(all_features), 'decision_tree')
        print("END DECISION TREE ONNX MODEL")

    # Train a Random Forest on the full dataset and export as .onnx
    def create_random_forest_model(self):
        print("CREATING RANDOM FOREST ONNX MODEL.....")
        print("CLASSIFICATION BASED ON THESE SENSORS: ", const.PROTOTYPE_SENSORS)
        all_features, all_classes = self.__get_full_dataset_for_classification()
        print("NUMBER OF FEATURES: ", len(all_features))
        classifier = RandomForestClassifier(n_estimators=const.PAR_RF_ESTIMATOR)
        classifier.fit(all_features, all_classes)
        self.__save_onnx(classifier, len(all_features), 'random_forest')
        print("END RANDOM FOREST ONNX MODEL")

    # Train a Neural Network (with scaler baked in) on the full dataset and export as .onnx
    def create_neural_network_model(self):
        print("CREATING NEURAL NETWORK ONNX MODEL.....")
        print("CLASSIFICATION BASED ON THESE SENSORS: ", const.PROTOTYPE_SENSORS)
        all_features, all_classes = self.__get_full_dataset_for_classification()
        print("NUMBER OF FEATURES: ", len(all_features))
        # Wrap scaler + classifier in a Pipeline so scaling is baked into the ONNX graph
        classifier = Pipeline([
            ('scaler', StandardScaler()),
            ('mlp', MLPClassifier(
                hidden_layer_sizes=const.PAR_NN_NEURONS,
                alpha=const.PAR_NN_ALPHA,
                max_iter=const.PAR_NN_MAX_ITER,
                tol=const.PAR_NN_TOL
            ))
        ])
        classifier.fit(all_features, all_classes)
        self.__save_onnx(classifier, len(all_features), 'neural_network')
        print("END NEURAL NETWORK ONNX MODEL")

    # Train an SVM (with scaler baked in) on the full dataset and export as .onnx
    def create_support_vector_machine_model(self, sensors_set):
        print("CREATING SUPPORT VECTOR MACHINE ONNX MODEL.....")
        print("CLASSIFICATION BASED ON THESE SENSORS: ", const.PROTOTYPE_SENSORS)
        all_features, all_classes = self.__get_full_dataset_for_classification()
        print("NUMBER OF FEATURES: ", len(all_features))
        # Wrap scaler + classifier in a Pipeline so scaling is baked into the ONNX graph
        classifier = Pipeline([
            ('scaler', StandardScaler()),
            ('svc', SVC(
                C=const.PAR_SVM_C,
                gamma=const.PAR_SVM_GAMMA,
                verbose=False
            ))
        ])
        classifier.fit(all_features, all_classes)
        self.__save_onnx(classifier, len(all_features), 'support_vector_machine')
        print("END SUPPORT VECTOR MACHINE ONNX MODEL")

if __name__ == "__main__":
	detection = TMDetection()

# --- ONNX export: train on full dataset (train+test) and save .onnx files ---
#	detection.create_decision_tree_model()
	detection.create_random_forest_model()
#	detection.create_neural_network_model()
#	detection.create_support_vector_machine_model()

