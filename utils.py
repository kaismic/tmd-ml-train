import pathlib

def get_transport_mode_from_path(path: pathlib.Path) -> str:
    """
    Extract the transport mode from the file name.
    The file name format is expected to be: sensorfile_<user_id>_<transport_mode>_<timestamp>.csv
    """
    return path.name.split("_")[2].lower()
