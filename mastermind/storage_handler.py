import glob
import json
import os
from typing import Any


class UserData:
    """Static class to store user configs in a single file."""

    _data = {}  # Class-level dictionary to hold user data
    _file_path = "data/userdata.config"  # Path to the user data file

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        """Ensure the data directory exists."""
        # Create the 'data' directory if it does not already exist
        os.makedirs("data", exist_ok=True)

    @classmethod
    def _load_data(cls) -> None:
        """Load user data from the config file."""
        cls._ensure_directory_exists()  # Ensure the directory is created
        # Check if the user data file exists
        if os.path.exists(cls._file_path):
            with open(cls._file_path, "r") as file:  # Open the file for reading
                cls._data = json.load(file)  # Load JSON data into the dictionary
        else:
            cls._data = {}  # Initialize to empty dict if wil doesn't exist

    @classmethod
    def save_data(cls) -> None:
        """Save user data to the config file."""
        cls._ensure_directory_exists()  # Ensure the directory is created
        with open(cls._file_path, "w") as file:  # Open the file for writing
            json_string = json.dumps(cls._data)  # Serialize dict to JSON string
            file.write(json_string)  # Write the entire string to the file

    @classmethod
    def clear_all(cls) -> None:
        """Clear all user data."""
        cls._data.clear()  # Clear the dictionary
        cls.save_data()  # Save the empty dictionary to the file

    @classmethod
    def __getattr__(cls, key: str) -> Any:
        """Allow access to keys in the data dictionary."""
        # If the requested key exists in the data, return its value; otherwise, return None
        if key in cls._data:
            return cls._data[key]
        return None

    @classmethod
    def __setattr__(cls, key: str, value: Any) -> None:
        """Allow direct modification of keys in the data dictionary."""
        cls._data[key] = value  # Add or update the key-value pair in the dictionary
        cls.save_data()  # Save the updated dictionary to the file


# Load existing data when the class is imported
UserData._load_data()


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
