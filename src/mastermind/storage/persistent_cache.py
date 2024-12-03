import glob
import os
from typing import Any

from mastermind.storage.pickle_io import (
    read_pickled_data,
    write_pickled_data,
)


class PersistentCacheManager:
    """
    Manages a persistent cache of Python objects on the file system.

    The PersistentCacheManager class provides a simple interface for caching and retrieving data,
    using the pickle_io module for pickling to serialize and deserialize the objects.

    The cache files are stored in the "data" directory, which is created automatically if it does not exist.
    """

    _cache_directory = "data"  # Directory to store cache files

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        """This method creates the cache directory if it does not already exist."""

        os.makedirs(cls._cache_directory, exist_ok=True)

    @classmethod
    def _get_cache_file_path(cls, key: str) -> str:
        """
        Returns the file path for a cache file based on the given key.

        Args:
            key (str): The key associated with the cache file.

        Returns:
            str: The file path for the cache file.
        """
        return os.path.join(cls._cache_directory, f"{key}.cache")

    @classmethod
    def clear_all_cache(cls) -> None:
        """Clears the entire cache by deleting all cache files."""
        for cache_file in glob.glob(os.path.join(cls._cache_directory, "*.cache")):
            os.remove(cache_file)

    @classmethod
    def __getattr__(cls, key: str) -> Any:
        """
        Retrieves the cached value for the given key, or None if the key does not exist.

        Args:
            key (str): The key associated with the cached value.

        Returns:
            Any: The cached value, or None if the key does not exist.
        """
        return read_pickled_data(cls._get_cache_file_path(key))

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Sets the cached value for the given key.

        Args:
            key (str): The key associated with the cached value.
            value (Any): The value to be cached.
        """
        write_pickled_data(cls._get_cache_file_path(key), value)
