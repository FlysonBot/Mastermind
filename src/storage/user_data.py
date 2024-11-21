import os
import pickle
from typing import Any


class UserDataManager:
    """
    A singleton class to manage user data storage and retrieval.

    This class provides a centralized way to load, save, and manipulate
    user data from a configuration file. It ensures that only one instance
    of the class exists and allows access to user data through dynamic attributes.

    Attributes:
        _instance (UserData): The singleton instance of the UserData class.
        _data (dict): A dictionary to hold user data.
        _file_path (str): The path to the user data configuration file.

    Examples:
        user_data = UserData()
        user_data.username = "JohnDoe"
        user_data["email"] = "john@example.com"
        print(user_data.username)
        print(user_data["email"])
    """

    _instance = None  # Class-level attribute for the singleton instance
    _data = {}  # Dictionary to hold user data
    _file_path = "data/userdata.config"  # Path to the user data file

    def __new__(cls) -> "UserDataManager":
        """Return the single instance of the UserData class."""
        if cls._instance is None:
            cls._instance = super(UserDataManager, cls).__new__(cls)
            cls._instance._load_data()  # Load data on instantiation
        return cls._instance

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        """Ensure the data directory exists."""
        os.makedirs("data", exist_ok=True)

    def _load_data(self) -> None:
        """Load user data from the config file using pickle."""
        self._ensure_directory_exists()  # Ensure the directory is created
        try:
            with open(self._file_path, "rb") as file:
                self._data = pickle.load(file)

        except FileNotFoundError:  # on first run
            self._data = {}

    def save_data(self) -> None:
        """Save user data to the config file using pickle."""
        self._ensure_directory_exists()  # Ensure the directory is created
        with open(self._file_path, "wb") as file:
            pickle.dump(self._data, file)

    def clear_all(self) -> None:
        """Clear all user data."""
        self._data.clear()
        self.save_data()

    def _retrieve_item(self, key: str) -> Any:
        """Retrieve an item from the data dictionary."""
        return self._data[key] if key in self._data else None

    def _modify_item(self, key: str, value: Any) -> None:
        """Modify an item in the data dictionary."""
        if key in {
            "_instance",
            "_data",
            "_file_path",
        }:  # Prevent overriding class attributes
            super().__setattr__(key, value)
        else:
            self._data[key] = value
            self.save_data()

    def __getattr__(self, key: str) -> Any:
        """
        Retrieve a value from the data dictionary based on the provided key.
        Allow for direct retrieval using dot notation.
        Return None if key doesn't exist.
        """
        return self._retrieve_item(key)

    def __getitem__(self, key: str) -> Any:
        """
        Retrieve a value from the data dictionary based on the provided key.
        Allow for retrieval using square bracket notation.
        Return None if key doesn't exist.
        """
        return self._retrieve_item(key)

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Modify a value from the data dictionary based on the provided key.
        Allow for direct modification using dot notation.
        """
        self._modify_item(key, value)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Modify a value from the data dictionary based on the provided key.
        Allow for modification using square bracket notation.
        """
        self._modify_item(key, value)

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the data dictionary."""
        return key in self._data
