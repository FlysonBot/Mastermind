from collections.abc import Callable
from functools import partial
from typing import Any

from mastermind.storage.pickle_io import (
    delete_pickled_data,
    read_pickled_data,
    write_pickled_data,
)

_user_data = None  # Variable to hold user data dictionary


class UserDataManager:
    """
    Manages user data with a customizable data storage interface. You should not use this class directly. Use get_user_data_manager() instead.

    This class wraps a data dictionary and provides methods to modify, retrieve, and clear user data, while ensuring that changes are saved through a provided save function.
    """

    def __init__(self, data: dict, save_fn: Callable[[dict], None]) -> None:
        """
        Decorate the given data dictionary with the UserDataManager interface.

        Args:
            data (dict): The data dictionary to be decorated.
            save_fn (Callable[dict, None]): A function that saves the data dictionary.
        """
        super().__setattr__("_data", data)
        super().__setattr__("save_data", lambda: save_fn(data=self._data))

    def clear_all(self) -> None:
        """Clears all the user data and saves the changes."""
        self._data.clear()  # clear method ensure _data instance is the same
        self.save_data()

    def _retrieve_item(self, key: str) -> Any:
        """
        Retrieves the value associated with the given key, or None if the key does not exist.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            Any: The value associated with the key, or None if the key does not exist.
        """
        return self._data.get(key, None)

    def _modify_item(self, key: str, value: Any) -> None:
        """
        Modify the value associated with the given key in the internal dictionary.
        If the key is one of the instance attribute, it modify that instead.
        After modifying the internal dictionary, it saves the changes to the file.

        Args:
            key (str): The key to modify the value for.
            value (Any): The new value to associate with the key.
        """

        if key in {"_data", "save_data"} and hasattr(self, key):
            raise NotImplementedError(f"Modification of {key} attribute is forbidden.")
        self._data[key] = value
        self.save_data()

    def __contains__(self, key: str) -> bool:
        return key in self._data

    # Allow dot and bracket notation for accessing and modifying data
    def __getattr__(self, key: str) -> Any:
        return self._retrieve_item(key)

    def __getitem__(self, key: str) -> Any:
        return self._retrieve_item(key)

    def __setattr__(self, key: str, value: Any) -> None:
        self._modify_item(key, value)

    def __setitem__(self, key: str, value: Any) -> None:
        self._modify_item(key, value)


def _load_data_safely(filepath: str) -> dict:  # sourcery skip: extract-duplicate-method
    """Loads the pickled data from the specified file path. If the file doesn't exist, it return an empty dictionary. This method is 'safe' because it handles exceptions and provides a user-friendly error message.

    Args:
        filepath (str): The path to the file to load data from.

    Raises:
        RuntimeError: When the data to be loaded is corrupted.
    """

    try:
        data = read_pickled_data(filepath)
        return data if data is not None else {}

    except Exception as e:
        print("An unexpected error occurred while loading the data.")
        print(e)
        print("\nIf this issue persists, consider deleting the stored data.")

        if not _prompt_delete_data(filepath):
            raise RuntimeError("Data could not be loaded.") from e
        return {}


def _prompt_delete_data(filepath: str) -> bool:
    """Prompts the user to delete the stored data.

    Args:
        filepath (str): The path to the file to delete.

    Returns:
        bool: Whether the user wants to delete the stored data.
    """
    decision = input("Do you want to delete the stored data? (y/n): ")

    if decision.lower() != "y":
        return False

    delete_pickled_data(filepath)
    print("Data deleted successfully.")
    return True


def _update_user_data(filepath: str):
    """Load user data and update user_data variable if not initialized."""

    global _user_data  # global ensures only 1 user_data exists at any time

    if "_user_data" not in globals() or _user_data is None:
        _user_data = _load_data_safely(filepath)


def get_user_data_manager() -> UserDataManager:
    """Returns a new UserDataManager instance."""
    filepath = "data/user_data.pkl"
    _update_user_data(filepath)  # ensure UserDataManager always use the same user_data
    return UserDataManager(_user_data, partial(write_pickled_data, filepath))
