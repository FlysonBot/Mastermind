import glob
import json
import os
from typing import Any


class UserData:
    """Singleton class to store user configs in a single file."""

    _instance = None  # Class-level attribute for the singleton instance
    _data = {}  # Dictionary to hold user data
    _file_path = "data/userdata.config"  # Path to the user data file

    def __new__(cls) -> 'UserData':
        if cls._instance is None:
            cls._instance = super(UserData, cls).__new__(cls)
            cls._instance._load_data()  # Load data on instantiation
        return cls._instance

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        """Ensure the data directory exists."""
        os.makedirs("data", exist_ok=True)

    def _load_data(self) -> None:
        """Load user data from the config file."""
        self._ensure_directory_exists()  # Ensure the directory is created
        if os.path.exists(self._file_path):
            with open(self._file_path, "r") as file:
                self._data = json.load(file)
        else:
            self._data = {}

    def save_data(self) -> None:
        """Save user data to the config file."""
        self._ensure_directory_exists()  # Ensure the directory is created
        with open(self._file_path, "w") as file:
            json_string = json.dumps(self._data)
            file.write(json_string)

    def clear_all(self) -> None:
        """Clear all user data."""
        self._data.clear()
        self.save_data()

    def __getattr__(self, key: str) -> Any:
        """Allow access to keys in the data dictionary."""
        if key in self._data:
            return self._data[key]
        raise AttributeError(f"{key} not found.")

    def __setattr__(self, key: str, value: Any) -> None:
        """Allow direct modification of keys in the data dictionary."""
        if key in ['_instance', '_data', '_file_path']:  # Prevent overriding class attributes
            super().__setattr__(key, value)
        else:
            self._data[key] = value
            self.save_data()


class Cache:
    """Static class to store cache to speed up computation in multiple files."""

    _cache_directory = "data"  # Directory to store cache files

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        """Ensure the cache directory exists."""
        # Create the 'data' directory if it does not already exist
        os.makedirs(cls._cache_directory, exist_ok=True)

    @classmethod
    def _get_cache_file_path(cls, key: str) -> str:
        """Get the file path for the given cache key."""
        # Construct the full path for the cache file corresponding to the key
        # i.e Cache.key will be stored in data/key.cache
        return os.path.join(cls._cache_directory, f"{key}.cache")

    @classmethod
    def clear_cache(cls) -> None:
        """Clear all cache files."""
        # Remove all cache files in the 'data' directory matching the *.cache pattern
        for cache_file in glob.glob(os.path.join(cls._cache_directory, "*.cache")):
            os.remove(cache_file)  # Delete the cache file

    @classmethod
    def __getattr__(cls, key: str) -> Any:
        """Allow direct access to cache keys."""
        file_path = cls._get_cache_file_path(key)  # Get the cache file path for the key
        # Check if the cache file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as file:  # Open the cache file for reading
                return file.read()  # Return the contents of the cache file
        return None  # Return None if the cache file does not exist

    @classmethod
    def set(cls, key: str, value: Any) -> Any:
        """Set a value in the cache."""
        file_path = cls._get_cache_file_path(key)  # Get the cache file path for the key
        with open(file_path, "w") as file:  # Open the cache file for writing
            file.write(value)  # Write the value to the cache file
