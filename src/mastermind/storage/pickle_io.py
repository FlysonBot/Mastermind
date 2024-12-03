import os
import pickle
from typing import Any


def read_pickled_data(filepath: str) -> Any:
    """Read pickled data from a file and return it.

    Args:
        filepath (str): The path to the file to read from.

    Returns:
        Any: The pickled data being read, or None if the file does not exist.
    """

    ensure_parent_directory_exists(filepath)
    try:
        with open(filepath, "rb") as file:
            return pickle.load(file)

    except FileNotFoundError:
        return None


def ensure_parent_directory_exists(filepath: str) -> None:
    """Create the parent directory of a file if it doesn't exist.

    Args:
        filepath (str): The path to the file.
    """
    if directory := os.path.dirname(filepath):
        os.makedirs(directory, exist_ok=True)

    else:
        raise ValueError("filepath must include a directory component")


def write_pickled_data(filepath: str, data: dict) -> None:
    """Write pickled data to a file.

    Args:
        filepath (str): The path to the file to write to.
        data (dict): The data to be pickled and written to the file.
    """

    ensure_parent_directory_exists(filepath)
    with open(filepath, "wb") as file:
        pickle.dump(data, file)


def delete_pickled_data(filepath: str) -> None:
    """Delete a pickled file.

    Args:
        filepath (str): The path to the file to delete.
    """
    os.remove(filepath)
