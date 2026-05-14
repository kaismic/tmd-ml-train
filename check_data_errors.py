import os
import csv
import re
import sys
from collections import defaultdict

csv.field_size_limit(2147483640)



print_limit = 10

def find_invalid_rows(folder_path):
    """
    Iterate through all CSV files in a folder and:
    - print rows where the first column is invalid
    - print summary statistics per file
    - count invalid rows by sensor type (second column)
    """

    # Matches positive whole numbers only
    positive_int_pattern = re.compile(r'^\d+$')

    # Statistics per file
    invalid_stats: dict[str, int] = {}

    # Statistics per sensor type
    invalid_sensor_counts: dict[str, int] = {}

    count = 0

    for filename in os.listdir(folder_path):
        # if count > 5:
        #     print("Stopping.")
        #     break
        # count += 1

        if not filename.endswith(".csv"):
            continue

        file_path = os.path.join(folder_path, filename)

        print(f"\nChecking file: {filename}")

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

            # Remove NUL characters while reading
            reader = csv.reader(
                (line.replace('\x00', '') for line in file)
            )

            for line_number, row in enumerate(reader, start=1):
                invalid = False

                # Empty row
                if not row or len(row) == 0:
                    invalid = True
                    reason = "Empty row"

                else:
                    first_value = row[0].strip()

                    # Missing first value
                    if not first_value:
                        invalid = True
                        reason = "Missing first value"

                    # Not a positive whole number
                    elif not positive_int_pattern.match(first_value):
                        invalid = True
                        reason = "Non-positive-whole-number"

                if invalid:

                    invalid_stats[filename] = invalid_stats.get(filename, 0) + 1

                    # Count second column values
                    if len(row) > 1:
                        second_column = row[1].strip()

                        # Only count actual sensor names
                        if (
                            second_column
                            and (
                                second_column.startswith("android.sensor.")
                                or second_column in ["sound", "speed"]
                            )
                        ):
                            invalid_sensor_counts[second_column] = invalid_sensor_counts.get(second_column, 0) + 1
                        else:
                            invalid_sensor_counts["<INVALID_SECOND_COLUMN>"] = invalid_sensor_counts.get("<INVALID_SECOND_COLUMN>", 0) + 1
                    else:
                        invalid_sensor_counts["<MISSING_SECOND_COLUMN>"] = invalid_sensor_counts.get("<MISSING_SECOND_COLUMN>", 0) + 1
                    # print(f"[INVALID] File: {filename} | Line: {line_number}")
                    # print(f"Reason: {reason}")
                    # print(f"Row: {row}")
                    # print()

    # =========================
    # Summary Per File
    # =========================
    print("\n====================")
    print("INVALID VALUE SUMMARY")
    print("====================")

    if not invalid_stats:
        print("No invalid rows found.")
    else:
        for filename, count in invalid_stats.items():
            print(f"{filename}: {count} invalid row(s)")

    # =========================
    # Invalid Sensor Counts
    # =========================
    print("\n====================")
    print("INVALID ROW COUNTS BY SECOND COLUMN")
    print("====================")

    if not invalid_sensor_counts:
        print("No invalid sensor values found.")
    else:
        for key, value in invalid_sensor_counts.items():
            print(f"{key}: {value}")

# Example usage
folder_path = r"d:/TCCT/vlomonaco/TransportationData/_RawDataOriginal/"
find_invalid_rows(folder_path)