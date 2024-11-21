import os
import pickle
from typing import Any


class UserDataManager:
    _instance = None  # Class-level attribute for the singleton instance
    _data = {}  # Dictionary to hold user data
    _file_path = "data/userdata.config"  # Path to the user data file

    def __new__(cls) -> "UserDataManager":
        if cls._instance is None:
            cls._instance = super(UserDataManager, cls).__new__(cls)
            cls._instance._load_data()  # Load data on instantiation
        return cls._instance

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        os.makedirs("data", exist_ok=True)

    def _load_data(self) -> None:
        self._ensure_directory_exists()  # Ensure the directory is created
        try:
            with open(self._file_path, "rb") as file:
                self._data = pickle.load(file)

        except FileNotFoundError:  # on first run
            self._data = {}

    def save_data(self) -> None:
        self._ensure_directory_exists()  # Ensure the directory is created
        with open(self._file_path, "wb") as file:
            pickle.dump(self._data, file)

    def clear_all(self) -> None:
        self._data.clear()
        self.save_data()

    def _retrieve_item(self, key: str) -> Any:
        return self._data[key] if key in self._data else None

    def _modify_item(self, key: str, value: Any) -> None:
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
        return self._retrieve_item(key)

    def __getitem__(self, key: str) -> Any:
        return self._retrieve_item(key)

    def __setattr__(self, key: str, value: Any) -> None:
        self._modify_item(key, value)

    def __setitem__(self, key: str, value: Any) -> None:
        self._modify_item(key, value)

    def __contains__(self, key: str) -> bool:
        return key in self._data
