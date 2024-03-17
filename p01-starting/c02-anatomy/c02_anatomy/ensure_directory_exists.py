import pathlib


def ensure_directory_exists(path_to_check):
    pathlib.Path(path_to_check).mkdir(parents=True, exist_ok=True)
