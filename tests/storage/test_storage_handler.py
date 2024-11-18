import os
import pickle
import unittest

from unittest.mock import mock_open, patch

from storage.storage_handler import Cache, UserData


class TestUserData(unittest.TestCase):
    """Test suite for the UserData class."""

    @patch(
        "builtins.open", new_callable=mock_open
    )  # Mock the open function to avoid actual file operations
    @patch(
        "os.path.exists"
    )  # Mock the os.path.exists function to simulate file existence
    @patch("os.makedirs")  # Mock os.makedirs to prevent actual directory creation
    def test_load_data_file_exists(self, mock_makedirs, mock_exists, mock_open):
        """Test loading data when the user data file exists."""
        mock_exists.return_value = True  # Simulate file existence

        # Simulate reading pickled data from the file
        mock_open.return_value.__enter__.return_value.read.return_value = pickle.dumps(
            {"key": "value"}
        )

        # Call the method to load data
        UserData()._load_data()

        # Check if the data was loaded correctly into the _data dictionary
        self.assertEqual(UserData()._data, {"key": "value"})

        # Verify directory creation was attempted
        mock_makedirs.assert_called_once()
        # Verify file was opened for reading in binary mode
        mock_open.assert_called_once_with(UserData()._file_path, "rb")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_load_data_file_not_exists(self, mock_makedirs, mock_exists, mock_open):
        """Test loading data when the user data file does not exist."""
        mock_exists.return_value = False  # Simulate that file does not exist

        # Call the method to load data
        UserData()._load_data()

        # Check that the data is initialized as an empty dictionary
        self.assertEqual(UserData()._data, {})

        # Verify directory creation
        mock_makedirs.assert_called_once()
        # Ensure the file was not opened since it doesn't exist
        mock_open.assert_not_called()

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_save_data(self, mock_makedirs, mock_open):
        """Test saving data to the user data file."""
        UserData()._data = {"key": "value"}  # Set some data to save

        UserData().save_data()  # Call the method to save data

        # Ensure directory was created
        mock_makedirs.assert_called_once()
        # Check that the file was opened for writing in binary mode
        mock_open.assert_called_once_with(UserData()._file_path, "wb")

        # Retrieve the file handle
        handle = mock_open()

        # Verify expected data was pickled and written
        expected_data = pickle.dumps({"key": "value"})  # Expected output
        handle.write.assert_called_once_with(expected_data)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_set_data(self, mock_makedirs, mock_open):
        """Test setting a new key-value pair in the user data."""
        UserData().new_key = "new_value"  # Set a new key-value pair

        # Verify new data is correctly stored
        self.assertEqual(UserData().new_key, "new_value")
        mock_open.assert_called_once_with(UserData()._file_path, "wb")

        # Retrieve the file handle and check the write calls
        handle = mock_open()
        expected_data = pickle.dumps(
            {"key": "value", "new_key": "new_value"}
        )  # Expected output
        handle.write.assert_called_once_with(expected_data)

    @patch("os.makedirs")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=pickle.dumps({"key": "value"}),
    )
    def test_clear_all(self, mock_open, mock_makedirs):
        """Test clearing all user data."""
        user_data = UserData()  # Initialize UserData, this will load the mock data

        # Ensure the initial data is loaded correctly
        self.assertEqual(user_data._data, {"key": "value"})

        # Call the method to clear all data
        user_data.clear_all()

        # Ensure data is cleared
        self.assertEqual(user_data._data, {})

        # Check that the file was opened for reading and writing
        self.assertEqual(mock_open.call_count, 2)  # Ensure open was called twice

        # Check that the first call was for reading
        mock_open.assert_any_call(user_data._file_path, "rb")

        # Check that the second call was for writing
        mock_open.assert_any_call(user_data._file_path, "wb")

        # Verify an empty dictionary was pickled and saved
        mock_open().write.assert_called_once_with(pickle.dumps({}))


class TestCache(unittest.TestCase):
    """Test suite for the Cache class."""

    @patch(
        "builtins.open", new_callable=mock_open
    )  # Mock the open function to avoid file operations
    @patch("os.makedirs")  # Mock os.makedirs to prevent actual directory creation
    def test_set_cache(self, mock_makedirs, mock_open):
        """Test setting a value in the cache."""
        key = "test_key"  # Key for the cache entry
        value = "test_value"  # Value to be stored in the cache

        # Call the method to set a cache value
        Cache.set(key, value)

        # Build expected file path for the cache file
        expected_path = os.path.join(Cache._cache_directory, f"{key}.cache")
        # Verify file was opened for writing in binary mode
        mock_open.assert_called_once_with(expected_path, "wb")
        # Check value was correctly pickled and written to the file
        mock_open().write.assert_called_once_with(pickle.dumps(value))

    @patch(
        "builtins.open", new_callable=mock_open
    )  # Mock open to simulate file reading
    @patch("os.path.exists")  # Mock to check file existence
    @patch("os.makedirs")  # Mock directory creation
    def test_get_cache_exists(self, mock_makedirs, mock_exists, mock_open):
        """Test retrieving a value from the cache when the file exists."""
        key = "test_key"  # Key to retrieve from the cache
        mock_exists.return_value = True  # Simulate that cache file exists

        # Simulate reading from the cache file
        mock_open.return_value.__enter__.return_value.read.return_value = pickle.dumps(
            "cached_value"
        )

        # Call the method to get the cache value
        result = Cache.__getattr__(key)

        # Build expected file path for the cache file
        expected_path = os.path.join(Cache._cache_directory, f"{key}.cache")
        # Check returned result matches expected cached value
        self.assertEqual(result, "cached_value")
        # Verify cache file was opened for reading in binary mode
        mock_open.assert_called_once_with(expected_path, "rb")

    @patch("os.path.exists")  # Mock to check file existence
    def test_get_cache_not_exists(self, mock_exists):
        """Test retrieving a value from the cache when the file does not exist."""
        key = "nonexistent_key"  # Key that does not exist in the cache
        mock_exists.return_value = False  # Simulate cache file does not exist

        # Call the method to get the cache value
        result = Cache.__getattr__(key)

        # Ensure None is returned when the file does not exist
        self.assertIsNone(result)

    @patch("glob.glob")  # Mock the glob function to simulate file listing
    @patch("os.remove")  # Mock os.remove to avoid file deletion
    def test_clear_cache(self, mock_remove, mock_glob):
        """Test clearing all cache files."""
        # Simulate two cache files exist
        mock_glob.return_value = ["data/test1.cache", "data/test2.cache"]

        # Call method to clear cache
        Cache.clear_cache()

        # Verify remove function was called for both files
        self.assertEqual(mock_remove.call_count, 2)


if __name__ == "__main__":
    unittest.main()
