import os
import pickle
import tempfile
import unittest
from unittest.mock import patch

from src.storage.user_data import UserDataManager


class TestUserDataManager(unittest.TestCase):
    """Test suite for the UserDataManager class"""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.file_path = os.path.join(cls.temp_dir.name, "userdata.config")
        UserDataManager._file_path = cls.file_path

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()
        UserDataManager._file_path = "data/userdata.config"

    def setUp(self):
        self.test_data = {"test_key": "test_value", "another_key": 42}

    def test_singleton(self):
        """Test that the UserDataManager is a singleton"""
        instance1 = UserDataManager()
        instance2 = UserDataManager()
        self.assertIs(instance1, instance2)

    def test_load_data(self):
        """Test that data is loaded from the file"""
        with patch(
            "builtins.open",
            unittest.mock.mock_open(read_data=pickle.dumps(self.test_data)),
        ):
            manager = UserDataManager()
            manager._load_data()
            self.assertEqual(manager._data, self.test_data)

        with patch(
            "builtins.open", unittest.mock.mock_open(read_data=b"corrupted data")
        ):
            manager = UserDataManager()
            self.assertRaises(pickle.UnpicklingError, manager._load_data)

    def test_save_data(self):
        """Test that data is saved to the file"""
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            manager = UserDataManager()
            manager._data = self.test_data
            manager.save_data()
            mock_file().write.assert_called_with(pickle.dumps(self.test_data))

            with self.assertRaises(PermissionError):
                mock_file.side_effect = PermissionError()
                manager = UserDataManager()
                manager.save_data()

    def test_clear_all(self):
        """Test that all data can be cleared"""
        manager = UserDataManager()
        manager._data = self.test_data
        manager.clear_all()
        self.assertEqual(manager._data, {})
        self.assertTrue(os.path.exists(self.file_path))

    def test_retrieve_item(self):
        """Test that items can be retrieved from the data"""
        manager = UserDataManager()
        manager._data = self.test_data
        self.assertEqual(manager._retrieve_item("test_key"), "test_value")
        self.assertIsNone(manager._retrieve_item("non_existent_key"))

    def test_modify_item(self):
        """Test that items can be modified in the data"""
        manager = UserDataManager()
        manager._data = self.test_data
        manager._modify_item("test_key", "new_value")
        self.assertEqual(manager._data["test_key"], "new_value")
        self.assertTrue(os.path.exists(self.file_path))

    def test_getattr_and_setattr(self):
        """Test that the __getattr__ and __setattr__ methods work as expected"""
        manager = UserDataManager()
        manager.test_attr = "test_value"
        self.assertEqual(manager.test_attr, "test_value")
        self.assertTrue(os.path.exists(self.file_path))

    def test_getitem_and_setitem(self):
        """Test that the __getitem__ and __setitem__ methods work as expected"""
        manager = UserDataManager()
        manager["test_key"] = "test_value"
        self.assertEqual(manager["test_key"], "test_value")
        self.assertTrue(os.path.exists(self.file_path))

    def test_contains(self):
        """Test that the __contains__ method works as expected"""
        manager = UserDataManager()
        manager._data = self.test_data
        self.assertTrue("test_key" in manager)
        self.assertFalse("non_existent_key" in manager)


if __name__ == "__main__":
    unittest.main()
