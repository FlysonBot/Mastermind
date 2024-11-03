import unittest  # Module for writing and running unit tests
from unittest.mock import patch, mock_open, MagicMock  # Mocks for testing
import os  # Module for interacting with the operating system
import json  # Module for working with JSON data
import glob  # Module for file pattern matching
from typing import Any  # Type hint for any value

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
            with open(cls._file_path, 'r') as file:  # Open the file for reading
                cls._data = json.load(file)  # Load JSON data into the dictionary
        else:
            cls._data = {}  # If the file doesn't exist, initialize as an empty dictionary

    @classmethod
    def _save_data(cls) -> None:
        """Save user data to the config file."""
        cls._ensure_directory_exists()  # Ensure the directory is created
        with open(cls._file_path, 'w') as file:  # Open the file for writing
            json_string = json.dumps(cls._data)  # Serialize the dictionary to a JSON string
            file.write(json_string)  # Write the entire string to the file

    @classmethod
    def clear_all(cls) -> None:
        """Clear all user data."""
        cls._data.clear()  # Clear the dictionary
        cls._save_data()  # Save the empty dictionary to the file

    @classmethod
    def __getattr__(cls, key: str) -> Any:
        """Allow access to keys in the data dictionary."""
        # If the requested key exists in the data, return its value; otherwise, return None
        if key in cls._data:
            return cls._data[key]
        return None

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set a value in the user data dictionary."""
        cls._data[key] = value  # Add or update the key-value pair in the dictionary
        cls._save_data()  # Save the updated dictionary to the file

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
            with open(file_path, 'r') as file:  # Open the cache file for reading
                return file.read()  # Return the contents of the cache file
        return None  # Return None if the cache file does not exist

    @classmethod
    def set(cls, key: str, value: Any) -> Any:
        """Set a value in the cache."""
        file_path = cls._get_cache_file_path(key)  # Get the cache file path for the key
        with open(file_path, 'w') as file:  # Open the cache file for writing
            file.write(value)  # Write the value to the cache file


# Testing
if __name__ == "__main__":

    class TestUserData(unittest.TestCase):
        """Test suite for the UserData class."""

        @patch('builtins.open', new_callable=mock_open)  # Mock the open function to avoid actual file operations
        @patch('os.path.exists')  # Mock the os.path.exists function to simulate file existence
        @patch('os.makedirs')  # Mock os.makedirs to prevent actual directory creation
        def test_load_data_file_exists(self, mock_makedirs, mock_exists, mock_open):
            """Test loading data when the user data file exists."""
            # Setup the mock to simulate the existence of the file
            mock_exists.return_value = True
            
            # Simulate reading JSON data from the file
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({'key': 'value'})

            # Call the method to load data
            UserData._load_data()

            # Check if the data was loaded correctly into the _data dictionary
            self.assertEqual(UserData._data, {'key': 'value'})
            
            # Verify that the directory creation was attempted
            mock_makedirs.assert_called_once()
            # Verify that the file was opened for reading
            mock_open.assert_called_once_with(UserData._file_path, 'r')

        @patch('builtins.open', new_callable=mock_open)
        @patch('os.path.exists')
        @patch('os.makedirs')
        def test_load_data_file_not_exists(self, mock_makedirs, mock_exists, mock_open):
            """Test loading data when the user data file does not exist."""
            # Simulate that the file does not exist
            mock_exists.return_value = False

            # Call the method to load data
            UserData._load_data()

            # Check that the data is initialized as an empty dictionary
            self.assertEqual(UserData._data, {})
            
            # Verify that the directory was created
            mock_makedirs.assert_called_once()
            # Ensure that the file was not opened since it doesn't exist
            mock_open.assert_not_called()

        @patch('builtins.open', new_callable=mock_open)
        @patch('os.makedirs')
        def test_save_data(self, mock_makedirs, mock_open):
            """Test saving data to the user data file."""
            UserData._data = {'key': 'value'}  # Set some data to save
            
            UserData._save_data()  # Call the method to save data

            # Ensure the directory was created
            mock_makedirs.assert_called_once()
            # Check that the file was opened for writing
            mock_open.assert_called_once_with(UserData._file_path, 'w')

            # Retrieve the file handle
            handle = mock_open()
            
            # Verify that the expected data was written (check the call list)
            expected_data = json.dumps({'key': 'value'})  # Prepare the expected output
            write_calls = handle.write.call_args_list  # Get the list of calls made to write

            # Check if the expected data was in the calls to write
            self.assertTrue(any(expected_data in str(call) for call in write_calls),
                            f"Expected write call with {expected_data} not found. Calls: {write_calls}")

        @patch('builtins.open', new_callable=mock_open)
        @patch('os.makedirs')
        def test_set_data(self, mock_makedirs, mock_open):
            """Test setting a new key-value pair in the user data."""
            UserData.set('new_key', 'new_value')  # Set a new key-value pair

            # Verify that the new data is correctly stored
            self.assertEqual(UserData._data['new_key'], 'new_value')
            mock_open.assert_called_once_with(UserData._file_path, 'w')

            # Retrieve the file handle and check the write calls
            handle = mock_open()
            
            expected_data = json.dumps({'key': 'value', 'new_key': 'new_value'})  # Prepare the expected output
            write_calls = handle.write.call_args_list  # Get the list of calls made to write
            
            # Check if the expected data was in the calls to write
            self.assertTrue(any(expected_data in str(call) for call in write_calls),
                            f"Expected write call with {expected_data} not found. Calls: {write_calls}")


        @patch('builtins.open', new_callable=mock_open)
        @patch('os.makedirs')
        def test_clear_all(self, mock_makedirs, mock_open):
            """Test clearing all user data."""
            # Initialize some data
            UserData._data = {'key': 'value'}
            
            # Call the method to clear all data
            UserData.clear_all()

            # Ensure the data is cleared
            self.assertEqual(UserData._data, {})
            # Check that the file was opened for writing (to save the empty data)
            mock_open.assert_called_once_with(UserData._file_path, 'w')
            # Verify that an empty dictionary was saved
            mock_open().write.assert_called_once_with(json.dumps({}))


    class TestCache(unittest.TestCase):
        """Test suite for the Cache class."""

        @patch('builtins.open', new_callable=mock_open)  # Mock the open function to avoid file operations
        @patch('os.makedirs')  # Mock os.makedirs to prevent actual directory creation
        def test_set_cache(self, mock_makedirs, mock_open):
            """Test setting a value in the cache."""
            key = 'test_key'  # Key for the cache entry
            value = 'test_value'  # Value to be stored in the cache
            
            # Call the method to set a cache value
            Cache.set(key, value)

            # Build the expected file path for the cache file
            expected_path = os.path.join(Cache._cache_directory, f"{key}.cache")
            # Verify that the file was opened for writing
            mock_open.assert_called_once_with(expected_path, 'w')
            # Check that the value was correctly written to the file
            mock_open().write.assert_called_once_with(value)

        @patch('builtins.open', new_callable=mock_open)  # Mock open to simulate file reading
        @patch('os.path.exists')  # Mock to check file existence
        @patch('os.makedirs')  # Mock directory creation
        def test_get_cache_exists(self, mock_makedirs, mock_exists, mock_open):
            """Test retrieving a value from the cache when the file exists."""
            key = 'test_key'  # Key to retrieve from the cache
            mock_exists.return_value = True  # Simulate that the cache file exists
            
            # Simulate reading from the cache file
            mock_open.return_value.__enter__.return_value.read.return_value = 'cached_value'

            # Call the method to get the cache value
            result = Cache.__getattr__(key)

            # Build the expected file path for the cache file
            expected_path = os.path.join(Cache._cache_directory, f"{key}.cache")
            # Check that the returned result matches the expected cached value
            self.assertEqual(result, 'cached_value')
            # Verify that the cache file was opened for reading
            mock_open.assert_called_once_with(expected_path, 'r')

        @patch('os.path.exists')  # Mock to check file existence
        def test_get_cache_not_exists(self, mock_exists):
            """Test retrieving a value from the cache when the file does not exist."""
            key = 'nonexistent_key'  # Key that does not exist in the cache
            mock_exists.return_value = False  # Simulate that the cache file does not exist

            # Call the method to get the cache value
            result = Cache.__getattr__(key)

            # Ensure that None is returned when the file does not exist
            self.assertIsNone(result)

        @patch('glob.glob')  # Mock the glob function to simulate file listing
        @patch('os.remove')  # Mock os.remove to avoid file deletion
        def test_clear_cache(self, mock_remove, mock_glob):
            """Test clearing all cache files."""
            # Simulate that two cache files exist
            mock_glob.return_value = ['data/test1.cache', 'data/test2.cache']
            
            # Call the method to clear the cache
            Cache.clear_cache()

            # Verify that the remove function was called for both files
            self.assertEqual(mock_remove.call_count, 2)


    unittest.main()