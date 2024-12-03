import unittest
from unittest.mock import mock_open, patch

from mastermind.storage.pickle_io import (
    delete_pickled_data,
    ensure_parent_directory_exists,
    read_pickled_data,
    write_pickled_data,
)


class TestPickleIO(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=b"{'key': 'value'}")
    @patch("mastermind.storage.pickle_io.pickle.load")
    def test_read_pickled_data_success(self, mock_pickle_load, mock_open_func):
        mock_pickle_load.return_value = {"key": "value"}
        data = read_pickled_data("data/data.pickle")
        self.assertEqual(data, {"key": "value"})
        mock_open_func.assert_called_once_with("data/data.pickle", "rb")
        mock_pickle_load.assert_called_once_with(
            mock_open_func.return_value.__enter__.return_value
        )

    @patch("mastermind.storage.pickle_io.open")
    def test_read_pickled_data_file_not_found(self, mock_open_func):
        mock_open_func.side_effect = FileNotFoundError
        data = read_pickled_data("data/data.pickle")
        self.assertIsNone(data)

    @patch("os.makedirs")
    def test_ensure_parent_directory_exists_success(self, mock_makedirs):
        ensure_parent_directory_exists("some/path/data.pickle")
        mock_makedirs.assert_called_once_with("some/path", exist_ok=True)

    def test_ensure_parent_directory_exists_raises_error(self):
        with self.assertRaises(ValueError):
            ensure_parent_directory_exists("data.pickle")

    @patch("builtins.open", new_callable=mock_open)
    @patch("mastermind.storage.pickle_io.pickle.dump")
    @patch("mastermind.storage.pickle_io.ensure_parent_directory_exists")
    def test_write_pickled_data_success(
        self, mock_ensure_directory, mock_pickle_dump, mock_open_func
    ):
        write_pickled_data("data.pickle", {"key": "value"})
        mock_ensure_directory.assert_called_once_with("data.pickle")
        mock_open_func.assert_called_once_with("data.pickle", "wb")
        mock_pickle_dump.assert_called_once_with(
            {"key": "value"}, mock_open_func.return_value.__enter__.return_value
        )

    @patch("os.remove")
    def test_delete_pickled_data_success(self, mock_remove):
        delete_pickled_data("data.pickle")
        mock_remove.assert_called_once_with("data.pickle")
