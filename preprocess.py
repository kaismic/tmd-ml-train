import argparse
import math
import re

import pandas as pd
import constants
import os
import csv
from tqdm import tqdm

# csv.field_size_limit(2**31 - 1)

def extract_raw_data() -> None:
    """
    Extract raw data from the downloaded tar.gz file.
    """
    raw_data_path = constants.DATA_PATH / constants.RAW_DATA_FILE_NAME

    if not os.path.isfile(raw_data_path):
        print(f"Raw data file not found at {raw_data_path}. Please download it first.")
        return

    print(f"Extracting raw data from {raw_data_path}...")

    import tarfile

    with tarfile.open(raw_data_path, "r:gz") as tar:
        tar.extractall(path=constants.DATA_PATH)

    print(f"Extraction complete. Extracted files are located at {constants.RAW_DATA_EXTRACTED_PATH}.")

def clean_file(input_path: os.PathLike, output_path: os.PathLike) -> None:
    """
    Clean a raw data file by:
    - Removing rows where the second column (sensor type) does not end with a valid sensor type
    """

    # int_pat = re.compile(r'^[-]?\d+$')

    with open(input_path, "r", encoding='utf-8', errors='replace') as input_file, \
         open(output_path, "w", encoding="utf-8", newline='') as output_file:

        reader = csv.reader(input_file)
        writer = csv.writer(output_file)

        for row in reader:
            if len(row) == 0:
                continue
            else:
                # TODO test if this works
                row = [re.sub(r'[^a-zA-Z0-9]', '', val) for val in row]
                remove: bool = False
                time: str = row[constants.RawDataFieldLocation.TIME.value]
                if not time:
                    remove = True
                elif not any(row[constants.RawDataFieldLocation.SENSOR_TYPE.value].endswith('.' + sensor) for sensor in constants.SENSORS):
                    remove = True

                if not remove:
                    # Remove leading '-' from time if present
                    # if time.startswith('-'):
                        # row[constants.RawDataFieldLocation.TIME.value] = time[1:]
                    writer.writerow(row)

def clean_files() -> None:
    """
    - Clean raw data files in the extracted folder and save cleaned versions in a new folder.
    - Select files to process based on transport modes defined in constants.TRANSPORT_MODES.
    """

    os.makedirs(constants.CLEANED_DATA_PATH, exist_ok=True)

    processing_files = list(constants.RAW_DATA_EXTRACTED_PATH.rglob("*.csv"))
    print(f"Total files to process: {len(processing_files)}")

    for input_path in tqdm(processing_files, desc="Cleaning files"):
        _, _, transport_mode, *_ = input_path.name.split("_")
        if transport_mode.lower() not in constants.TRANSPORT_MODES:
            continue

        output_file_path = constants.CLEANED_DATA_PATH / input_path.relative_to(constants.RAW_DATA_EXTRACTED_PATH)
        os.makedirs(output_file_path.parent, exist_ok=True)

        clean_file(input_path, output_file_path)

    print(f"Cleaning complete. Cleaned files are located at {constants.CLEANED_DATA_PATH}.")

def transform_file(input_path: os.PathLike, output_path: os.PathLike) -> None:
    """
    Transform a cleaned data file by:
    - Segmenting the data into overlapping windows of a specified size and step.
    - For each window, compute features (mean, std, min, max) for each sensor type.
    - For vector sensors, compute the magnitude of the vector and use that for feature computation instead of individual components.
    - For rotation vector, compute sin(θ/2) from the w component and use that for feature computation instead of the raw value.
    - Save the transformed features in a new CSV file with a header indicating the sensor and feature type.
    - The output CSV will have columns: time (window index), followed by features for each sensor in the order defined by constants.SENSOR_FEATURES_IN_ORDER.
    """

    with open(output_path, "w", encoding="utf-8", newline='') as output_file:
        writer = csv.writer(output_file)

        window_size_ms = int(constants.WINDOW_SIZE_SECONDS * 1000)
        window_next_step_ms = int(constants.WINDOW_NEXT_STEP_SECONDS * 1000)

        df = pd.read_csv(
            input_path,
            names=['time', 'sensor_type', 'val1', 'val2', 'val3', 'val4', 'val5']
        )

        print(df.head())

        curr_window_start: int = 0
        i: int = 0
        last_time: int = df['time'].iloc[-1]

        writer.writerow(['time'] + constants.SENSOR_FEATURES_IN_ORDER)

        while True:
            curr_window_end = curr_window_start + window_size_ms
            if curr_window_end > last_time:
                break
            window: pd.DataFrame = df[(df['time'] >= curr_window_start) & (df['time'] < curr_window_end)]
            for sensor in constants.SENSORS:
                transformed_features = {}
                transformed_values: pd.Series = pd.Series()
                valid: bool = False
                sensor_window: pd.DataFrame = window[window['sensor_type'] == sensor]
                if (not sensor_window.empty):
                    if (sensor in constants.VECTOR_TRANSFORM_SENSORS):
                        transformed_values = (sensor_window[['val1', 'val2', 'val3']].pow(2).sum(axis=1)).pow(0.5)
                        valid = True
                    elif (sensor in constants.SCALAR_TRANSFORM_SENSORS):
                        # Compute sin(θ/2) from w component of rotation vector
                        # But I'm not sure if this is even necessary or useful, since the rotation vector already represents orientation in a compact form.
                        transformed_values = sensor_window['val4'].apply(math.acos).apply(math.sin)
                        valid = True
                    if valid:
                        assert not transformed_values.empty, "Transformed values should not be empty when valid is True"
                        transformed_features[f"{sensor}#mean"] = transformed_values.mean()
                        transformed_features[f"{sensor}#std"] = transformed_values.std()
                        transformed_features[f"{sensor}#min"] = transformed_values.min()
                        transformed_features[f"{sensor}#max"] = transformed_values.max()
                        writer.writerow([i] + [transformed_features[sensor_feature] for sensor_feature in constants.SENSOR_FEATURES_IN_ORDER])
            curr_window_start += window_next_step_ms
            i += 1

def transform_files() -> None:
    """
    Transform cleaned data files into a format suitable for machine learning models.
    """
    os.makedirs(constants.TRANSFORMED_DATA_PATH, exist_ok=True)

    processing_files = list(constants.CLEANED_DATA_PATH.rglob("*.csv"))
    print(f"Total files to process for transformation: {len(processing_files)}")

    # for input_path in tqdm(processing_files, desc="Transforming files"):
    for input_path in processing_files:
        output_file_path = constants.TRANSFORMED_DATA_PATH / input_path.relative_to(constants.CLEANED_DATA_PATH)
        os.makedirs(output_file_path.parent, exist_ok=True)
        transform_file(input_path, output_file_path)

    print(f"Transformation complete. Transformed files are located at {constants.TRANSFORMED_DATA_PATH}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Extract and clean raw data files"
    )
    group.add_argument(
        "--extract",
        action="store_true",
        help="Extract raw data files"
    )
    group.add_argument(
        "--clean",
        action="store_true",
        help="Clean extracted raw data files"
    )
    group.add_argument(
        "--transform",
        action="store_true",
        help="Transform cleaned data files"
    )
    args = parser.parse_args()

    if args.extract or args.all:
        extract_raw_data()
    if args.clean or args.all:
        clean_files()
    if args.transform or args.all:
        transform_files()