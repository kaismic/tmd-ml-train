#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################## WORKING ###########################################
# if is set to false build new dataset from directory with original files collected from users
HAVE_DT = False
# if is set to true use sintetic data to train the model
SINTETIC_LEARNING = False

################################## Directories ########################################
# working directory
DIR_TM = './TransportationData'
# directory with original files collected from users
DIR_RAW_DATA_ORIGINAL = DIR_TM + '/_RawDataOriginal'
#DIR_RAW_DATA_ORIGINAL = DIR_TM + '/prova'
#DIR_RAW_DATA_ORIGINAL = DIR_TM + '/corrupted_rec'

# directory to fill with correct files
DIR_RAW_DATA_CORRECT = DIR_TM + '/_RawDataCorrect/'
# directory to fill with correct files and sensor data after transformations
DIR_RAW_DATA_TRANSFORM = DIR_TM + '/_RawDataTransform/'
# directory to fill with all file transformed according to dataset header
DIR_RAW_DATA_HEADER = DIR_TM + '/_RawDataHeader'
# directory to fill with all file transformed according to dataset header and features on time windows
DIR_RAW_DATA_FEATURES = DIR_TM + '/_RawDataFeatures'
# directory to fill with dataset file
DIR_DATASET = DIR_TM + '/_Dataset'
# directory to fill with sintetic dataset file
DIR_SINTETIC_RAW_DATASET = DIR_TM + '/_SinteticDatasetCorrect'
# directory to fill with correct sintetic files and sensor data after transformations
DIR_SINTETIC_RAW_DATA_TRANSFORM = DIR_TM + '/_SinteticRawDataTransform/'
# directory to fill with all file transformed according to dataset header
DIR_SINTETIC_RAW_DATA_HEADER = DIR_TM + '/_SinteticRawDataHeader/'
# directory to fill with all sintetic file transformed according to dataset header and features on time windows
DIR_SINTETIC_RAW_DATA_FEATURES = DIR_TM + '/_SinteticRawDataFeatures'
# directory to fill with dataset file
DIR_SINTETIC_DATASET = DIR_TM + '/_SinteticDataset'

# directory to fill with all results
DIR_RESULTS = './TransportationDetectionResults'

##################################### Files ###########################################
CLEAN_LOG = 'cleanLog.log'
# file for save users and sensors support
FILE_SUPPORT = 'sensors_support.csv'

# dataset file name
FILE_DATASET = "dataset.csv"
# sintetic dataset file name
SINTETIC_FILE_DATASET = "sinteticdataset.csv"

# balanced files name
FILE_DATASET_BALANCED = "dataset_balanced.csv"
FILE_TRAINING = "training_balanced.csv"
FILE_TEST = "test_balanced.csv"
FILE_CV = "cv_balanced.csv"
SINTETIC_FILE_TEST = "sintetic_test_balanced.csv"
SINTETIC_FILE_CV = "sintetic_cv_balanced.csv"
SINTETIC_FILE_DATASET_BALANCED = "sintetic_dataset_balanced.csv"
SINTETIC_FILE_TRAINING = "sintetic_training_balanced.csv"

# classification results
FILE_DECISION_TREE_RESULTS = "_decision_tree.csv"
FILE_RANDOM_FOREST_RESULTS = "_random_forest.csv"
FILE_NEURAL_NETWORK_RESULTS = "_neural_network.csv"
FILE_SUPPORT_VECTOR_MACHINE_RESULTS = "_support_vector_machine.csv"


# classification combination of classes results
FILE_TWO_CLASSES_COMBINATION = "_two_classes_combination.csv"

# leave one subject out results
FILE_LEAVE_ONE_SUBJECT_OUT = "_leave_one_subject_out.csv"

# single sensor analysis
FILE_SINGLE_SENSOR_ANALYSIS = "_single_sensors_accuracy.csv"
#######################################################################################

################################## Sensors #############################################
################## list of sensors to exclude for classification #######################

SENSORS_TO_EXCLUDE_FROM_DATASET = ['com.google.sensor.internal_temperature', 'com.qti.sensor.amd',
                                   'com.qti.sensor.rmd', 'android.sensor.tilt_detector',
                                   'android.sensor.geomagnetic_rotation_vector', 'android.sensor.step_detector',
                                   'android.sensor.gesture','android.sensor.step_counter','android.sensor.pressure','android.sensor.magnetic_field_uncalibrated','android.sensor.proximity','android.sensor.gravity','android.sensor.light','android.sensor.gesture','android.sensor.orientation','android.sensor.gyroscope_uncalibrated','activityrecognition','speed',]

# compute magnitude
SENSOR_TO_TRANSFORM_MAGNITUDE = ['android.sensor.accelerometer', 'android.sensor.orientation',
                                 'android.sensor.linear_acceleration', 'android.sensor.gyroscope',
                                 'android.sensor.magnetic_field', 'android.sensor.magnetic_field_uncalibrated',
                                 'android.sensor.gyroscope_uncalibrated', 'android.sensor.gravity']

# compute sin(θ/2)
SENSOR_TO_TRANSFROM_4ROTATION = ['android.sensor.rotation_vector',
                                 'android.sensor.game_rotation_vector']

# sensors for which it is relevant only the first data
SENSOR_TO_TAKE_FIRST = ['android.sensor.light', 'speed', 'android.sensor.proximity', 'android.sensor.pressure']

#######################################################################################

################################# Time Division ########################################
# dimension in second
WINDOW_DIMENSION = 5
# in our application every second the application write 10 model
SAMPLE_FOR_SECOND = 1000

#######################################################################################

################################# Split rules ########################################
TRAINING_PERC = 0.5
TEST_PERC = 0.5
CV_PERC = 0.0

#######################################################################################

###################### sensor classification levels ###################################
# sensor_to_exclude_first = ['com.google.sensor.internal_temperature',
#                            'com.qti.sensor.amd',
#                            'com.qti.sensor.rmd',
#                            'android.sensor.step_detector',
#                            'android.sensor.tilt_detector',
#                            'android.sensor.geomagnetic_rotation_vector',
#                            'android.sensor.step_counter',
#                            'android.sensor.pressure',
#                            'android.sensor.magnetic_field_uncalibrated',
#                            'android.sensor.proximity',
#                            'android.sensor.magnetic_field',
#                            'android.sensor.gravity',
#                            'android.sensor.light',
#                            'android.sensor.gesture',
#                            'android.sensor.linear_acceleration',
#                            'android.sensor.orientation',
#                            'android.sensor.rotation_vector',
#                            'android.sensor.game_rotation_vector',
#                            'android.sensor.gyroscope_uncalibrated',
#                            'activityrecognition',
#                            'speed',
#                            'time']

# sensor_to_exclude_second = ['com.google.sensor.internal_temperature',
#                             'com.qti.sensor.amd',
#                             'com.qti.sensor.rmd',
#                             'android.sensor.step_detector',
#                             'android.sensor.tilt_detector',
#                             'android.sensor.geomagnetic_rotation_vector',
#                             'android.sensor.step_counter',
#                             'android.sensor.pressure',
#                             'android.sensor.magnetic_field_uncalibrated',
#                             'android.sensor.proximity',
#                             'android.sensor.magnetic_field',
#                             'android.sensor.gravity',
#                             'android.sensor.light',
#                             'android.sensor.gesture',
#                             'speed',
#                             'activityrecognition',
#                             'time']

# sensors_to_exclude_third = ['com.google.sensor.internal_temperature',
#                             'com.qti.sensor.amd',
#                             'com.qti.sensor.rmd',
#                             'android.sensor.step_detector',
#                             'android.sensor.tilt_detector',
#                             'android.sensor.geomagnetic_rotation_vector',
#                             'android.sensor.step_counter',
#                             'android.sensor.pressure',
#                             'android.sensor.magnetic_field_uncalibrated',
#                             'android.sensor.proximity',
#                             'android.sensor.magnetic_field',
#                             'android.sensor.gravity',
#                             'android.sensor.light',
#                             'android.sensor.gesture',
#                             'activityrecognition',
#                             'time']


# 'gravity'
# 'android.sensor.game_rotation_vector'
# 'android.sensor.orientation'
# 'android.sensor.gyroscope_uncalibrated'
# 'sound'
# 'android.sensor.step_counter'
# 'android.sensor.proximity'
# 'android.sensor.pressure'
########################################################################################

###################### classification algorithms parameters ##############################
# repeat time for single sensors classification
REPEAT = 30

# random forest
PAR_RF_ESTIMATOR = 100
# neural network
PAR_NN_NEURONS = 880
PAR_NN_ALPHA = 0.000002
PAR_NN_MAX_ITER = 600
PAR_NN_TOL = -1
# support vector machine
PAR_SVM_C = 100
PAR_SVM_GAMMA = 0.1

################################### data type for dataset ##################################
DATASET_DATA_TYPE = {"user_id": int}




from pathlib import Path


DATA_PATH = Path.cwd() / "data"
RAW_DATA_FILE_NAME = "raw_data.tar.gz"
RAW_DATA_EXTRACTED_PATH = DATA_PATH / "raw_data"
CLEANED_DATA_PATH = DATA_PATH / "cleaned_data"
TRANSFORMED_DATA_PATH = DATA_PATH / "transformed_data"

TRANSPORT_MODES = ["bus", "car", "train"]

SENSORS = [
    'accelerometer',
    'gyroscope',
    'linear_acceleration',
    'magnetic_field',
    'rotation_vector'
]

# Compute magnitude from 3-axis
VECTOR_TRANSFORM_SENSORS = (
    'accelerometer',
    'gyroscope',
    'linear_acceleration',
    'magnetic_field'
)

# Compute sin(θ/2) from w component of rotation vector
SCALAR_TRANSFORM_SENSORS = (
    'rotation_vector'
)

FEATURES = ['mean', 'std', 'min', 'max']

SENSOR_FEATURES_IN_ORDER = [f"{sensor}#{feature}" for sensor in SENSORS for feature in FEATURES]

NA_THRESHOLD = 0.7

WINDOW_SIZE_SECONDS: float = 10
WINDOW_NEXT_STEP_SECONDS: float = 5

from enum import Enum

class RawDataFieldLocation(Enum):
    TIME = 0
    SENSOR_TYPE = 1