import glob
import os
import pickle
from typing import Any


class PersistentCache:
    """
    A class to manage caching of data using files.

    This class provides methods to store, retrieve, and clear cached data
    in a specified directory. It allows for easy access to cached values
    through dynamic attributes and ensures that the cache directory exists.

    Attributes:
        _cache_directory (str): The directory where cache files are stored.

    Examples:
        Cache.set("user_data", {"name": "John", "age": 30})
        user_data = Cache.user_data
    """

    _cache_directory = "data"  # Directory to store cache files

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        """Ensure the cache directory exists."""
        os.makedirs(cls._cache_directory, exist_ok=True)

    @classmethod
    def _get_cache_file_path(cls, key: str) -> str:
        """Get the file path for the given cache key."""
        return os.path.join(cls._cache_directory, f"{key}.cache")

    @classmethod
    def clear_cache(cls) -> None:
        """Clear all cache files."""
        for cache_file in glob.glob(os.path.join(cls._cache_directory, "*.cache")):
            os.remove(cache_file)

    @classmethod
    def __getattr__(cls, key: str) -> Any:
        """Allow direct access to cache keys using pickle."""
        file_path = cls._get_cache_file_path(key)
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                return pickle.load(file)
        return None

    @classmethod
    def set(cls, key: str, value: Any) -> Any:
        """Set a value in the cache using pickle."""
        with open(cls._get_cache_file_path(key), "wb") as file:
            pickle.dump(value, file)
