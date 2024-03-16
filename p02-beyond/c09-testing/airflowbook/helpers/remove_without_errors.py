import errno
import os


def remove_without_errors(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        if e.errno != errno.ENOENT:  # Ignore error if file does not exist
            raise  # Re-raise any other OSError
