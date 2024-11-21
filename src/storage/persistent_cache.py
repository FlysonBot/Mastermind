import glob
import os
import pickle
from typing import Any


class PersistentCacheManager:
    _cache_directory = "data"  # Directory to store cache files

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        os.makedirs(cls._cache_directory, exist_ok=True)

    @classmethod
    def _get_cache_file_path(cls, key: str) -> str:
        return os.path.join(cls._cache_directory, f"{key}.cache")

    @classmethod
    def clear_cache(cls) -> None:
        for cache_file in glob.glob(os.path.join(cls._cache_directory, "*.cache")):
            os.remove(cache_file)

    @classmethod
    def __getattr__(cls, key: str) -> Any:
        file_path = cls._get_cache_file_path(key)
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                return pickle.load(file)
        return None

    @classmethod
    def set(cls, key: str, value: Any) -> Any:
        with open(cls._get_cache_file_path(key), "wb") as file:
            pickle.dump(value, file)
