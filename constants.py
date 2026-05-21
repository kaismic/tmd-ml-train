from pathlib import Path

DATA_PATH = Path.cwd() / "data"
RAW_DATA_FILE_NAME = "raw_data.tar.gz"
RAW_DATA_EXTRACTED_PATH = DATA_PATH / "raw_data"
CLEANED_DATA_PATH = DATA_PATH / "cleaned_data"
TRANSFORMED_DATA_PATH = DATA_PATH / "transformed_data"
MODELS_PATH = Path.cwd() / "models"

TRANSPORT_MODES = {
    'bus': 0,
    'car': 1,
    'train': 2
}

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