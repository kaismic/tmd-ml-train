import argparse
import constants
import os
import csv
import re
from typing import Generator, TextIO
# from tqdm import tqdm

# csv.field_size_limit(2**31 - 1)
# print_limit = 10

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

def read_in_chunks(
    file_object: TextIO,
    chunk_size: int = 1024 * 1024
) -> Generator[str, None, None]:
    """
    Generator that reads a file in chunks.
    Default chunk size = 1 MB.
    """

    while True:
        chunk: list[str] = file_object.readlines(chunk_size)
        if not chunk:
            break
        for line in chunk:
            yield line

def clean_file(input: TextIO, output: TextIO) -> None:
    """
    Clean a raw data file by:
    - Removing rows where the first column (time) is empty or not a positive whole number
    - Removing rows where the second column (sensor type) does not end with a valid sensor type
    """
    # Matches positive whole numbers only
    positive_int_pattern = re.compile(r'^\d+$')

    # Read file in chunks
    chunk_reader = (line.replace('\x00', '') for line in read_in_chunks(input))
    reader = csv.reader(chunk_reader)
    writer = csv.writer(output)

    for _, row in enumerate(reader):
        remove: bool = False

        # Empty row
        if not row or len(row) == 0:
            remove = True
        else:
            time: str = row[constants.RawDataFieldLocation.TIME.value]
            if not time:
                remove = True
            # Not a positive whole number
            elif not positive_int_pattern.match(time):
                remove = True
            elif not any(row[constants.RawDataFieldLocation.SENSOR_TYPE.value].endswith(sensor) for sensor in constants.SENSORS):
                remove = True

        if not remove:
            writer.writerow(row)

def clean_files() -> None:
    """
    - Clean raw data files in the extracted folder and save cleaned versions in a new folder.
    - Select files to process based on transport modes defined in constants.TRANSPORT_MODES.
    """

    os.makedirs(constants.CLEANED_DATA_PATH, exist_ok=True)

    processing_files = list(constants.RAW_DATA_EXTRACTED_PATH.rglob("*.csv"))

    # Now you can safely check the len() of the list
    print(f"Total files to process: {len(processing_files)}")
    for input_path in processing_files:
        # print(f"Processing file: {input_path}")
        _, _, transport_mode, *_ = input_path.name.split("_")
        if transport_mode.lower() not in constants.TRANSPORT_MODES:
            continue

        output_file_path = constants.CLEANED_DATA_PATH / input_path.relative_to(constants.RAW_DATA_EXTRACTED_PATH)
        os.makedirs(output_file_path.parent, exist_ok=True)

        with open(input_path, "r", encoding="utf-8", errors="ignore") as input_file, \
             open(output_file_path, "x", encoding="utf-8", newline='') as output_file:
            clean_file(input_file, output_file)

    print(f"Cleaning complete. Cleaned files are located at {constants.CLEANED_DATA_PATH}.")

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
    args = parser.parse_args()

    if args.extract or args.all:
        extract_raw_data()
    if args.clean or args.all:
        clean_files()