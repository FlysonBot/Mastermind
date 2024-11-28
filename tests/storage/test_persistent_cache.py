import os
import unittest
import tempfile

from src.storage.persistent_cache import PersistentCacheManager


class TestPersistentCacheManager(unittest.TestCase):
    """Test suite for the PersistentCacheManager class"""

    @classmethod
    def setUpClass(cls):
        # Set up a temporary cache directory for testing
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.cache_dir = os.path.join(cls.temp_dir.name, "cache")
        PersistentCacheManager._cache_directory = cls.cache_dir

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()
        PersistentCacheManager._cache_directory = "data"

    def test_ensure_directory_exists(self):
        """Test that the cache directory is created if it does not exist"""
        os.rmdir(self.cache_dir)
        self.assertFalse(os.path.exists(self.cache_dir))
        PersistentCacheManager._ensure_directory_exists()
        self.assertTrue(os.path.exists(self.cache_dir))
        PersistentCacheManager._ensure_directory_exists()
        self.assertTrue(os.path.exists(self.cache_dir))

    def test_get_cache_file_path(self):
        """Test that the correct cache file path is generated"""
        test_key = "test_key"
        file_path = PersistentCacheManager._get_cache_file_path(test_key)
        expected_path = os.path.join(self.cache_dir, f"{test_key}.cache")
        self.assertEqual(file_path, expected_path)

    def test_set_and_get_within_instance(self):
        """Test that values can be set and retrieved within the same instance"""
        test_key = "test_key"
        test_value = {"data": [1, 2, 3]}
        manager = PersistentCacheManager()
        manager.set(test_key, test_value)
        retrieved_value = manager.__getattr__(test_key)
        self.assertEqual(retrieved_value, test_value)

    def test_persistence_across_instances(self):
        """Test that values persist across different instances of PersistentCacheManager"""
        test_key = "test_key"
        test_value = {"data": [1, 2, 3]}

        # Set value with the first instance
        first_manager = PersistentCacheManager()
        first_manager.set(test_key, test_value)

        # Retrieve value with a new instance
        second_manager = PersistentCacheManager()
        retrieved_value = second_manager.__getattr__(test_key)
        self.assertEqual(retrieved_value, test_value)

    def test_get_non_existent_key(self):
        """Test that getting a non-existent key returns None"""
        self.assertIsNone(PersistentCacheManager.__getattr__("non_existent_key"))

    def test_clear_cache(self):
        """Test that the cache can be cleared"""
        test_key = "test_key"
        test_value = {"data": [1, 2, 3]}
        PersistentCacheManager._ensure_directory_exists()
        PersistentCacheManager.set(test_key, test_value)
        self.assertIsNotNone(PersistentCacheManager.__getattr__(test_key))
        PersistentCacheManager.clear_cache()
        self.assertIsNone(PersistentCacheManager.__getattr__(test_key))


if __name__ == "__main__":
    unittest.main()
