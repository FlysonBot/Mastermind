import unittest
from unittest.mock import MagicMock, patch

from mastermind.storage.user_data import (
    UserDataManager,
    _load_data_safely,
    _prompt_delete_data,
)


class TestUserDataManager(unittest.TestCase):
    def setUp(self):
        self.test_data = {"key1": "value1", "key2": "value2"}
        self.save_fn = MagicMock()
        self.user_data_manager = UserDataManager(self.test_data, self.save_fn)

    def test_clear_all(self):
        self.user_data_manager.clear_all()
        self.assertEqual(self.user_data_manager._data, {})
        self.save_fn.assert_called_once_with(data={})

    def test_retrieve_item_existing_key(self):
        self.assertEqual(self.user_data_manager._retrieve_item("key1"), "value1")

    def test_retrieve_item_non_existing_key(self):
        self.assertIsNone(self.user_data_manager._retrieve_item("non_existent_key"))

    def test_modify_item_valid_key(self):
        self.user_data_manager._modify_item("key1", "new_value")
        self.assertEqual(self.user_data_manager._data["key1"], "new_value")
        self.save_fn.assert_called_once_with(data=self.test_data)

    def test_modify_item_protected_key(self):
        with self.assertRaises(NotImplementedError):
            self.user_data_manager._modify_item("_data", "new_value")

    def test_getattr_existing_key(self):
        self.assertEqual(self.user_data_manager.key1, "value1")

    def test_getattr_non_existing_key(self):
        self.assertIsNone(self.user_data_manager.non_existent_key)

    def test_getitem_existing_key(self):
        self.assertEqual(self.user_data_manager["key1"], "value1")

    def test_getitem_non_existing_key(self):
        self.assertIsNone(self.user_data_manager["non_existent_key"])

    def test_setattr_valid_key(self):
        self.user_data_manager.key1 = "new_value"
        self.assertEqual(self.user_data_manager._data["key1"], "new_value")
        self.save_fn.assert_called_once_with(data=self.test_data)

    def test_setattr_protected_key(self):
        with self.assertRaises(NotImplementedError):
            self.user_data_manager._data = "new_value"

    def test_setitem_valid_key(self):
        self.user_data_manager["key1"] = "new_value"
        self.assertEqual(self.user_data_manager._data["key1"], "new_value")
        self.save_fn.assert_called_once_with(data=self.test_data)

    def test_setitem_protected_key(self):
        with self.assertRaises(NotImplementedError):
            self.user_data_manager["_data"] = "new_value"

    def test_contains_existing_key(self):
        self.assertTrue("key1" in self.user_data_manager)

    def test_contains_non_existing_key(self):
        self.assertFalse("non_existent_key" in self.user_data_manager)


class TestLoadData(unittest.TestCase):
    @patch("mastermind.storage.user_data.read_pickled_data")
    def test_load_data_file_exists(self, mock_read_pickled_data):
        mock_read_pickled_data.return_value = {"key1": "value1"}
        data = _load_data_safely("data.pickle")
        self.assertEqual(data, {"key1": "value1"})

    @patch("mastermind.storage.user_data.read_pickled_data")
    def test_load_data_file_not_exists(self, mock_read_pickled_data):
        mock_read_pickled_data.return_value = None
        data = _load_data_safely("data.pickle")
        self.assertEqual(data, {})

    @patch("mastermind.storage.user_data.read_pickled_data")
    @patch("mastermind.storage.user_data._prompt_delete_data")
    def test_load_data_file_corrupted(
        self, mock_prompt_delete_data, mock_read_pickled_data
    ):
        mock_read_pickled_data.side_effect = Exception("Corrupt data")
        mock_prompt_delete_data.return_value = True
        data = _load_data_safely("data.pickle")
        self.assertEqual(data, {})

    @patch("mastermind.storage.user_data.read_pickled_data")
    @patch("mastermind.storage.user_data._prompt_delete_data")
    def test_load_data_file_corrupted_user_declines_delete(
        self, mock_prompt_delete_data, mock_read_pickled_data
    ):
        mock_read_pickled_data.side_effect = Exception("Corrupt data")
        mock_prompt_delete_data.return_value = False
        with self.assertRaises(RuntimeError):
            _load_data_safely("data.pickle")


class TestPromptDeleteData(unittest.TestCase):
    @patch("builtins.input", return_value="y")
    @patch("mastermind.storage.user_data.delete_pickled_data")
    def test_prompt_delete_data_user_confirms(
        self, mock_delete_pickled_data, mock_input
    ):
        self.assertTrue(_prompt_delete_data("data.pickle"))
        mock_delete_pickled_data.assert_called_once_with("data.pickle")

    @patch("builtins.input", return_value="n")
    def test_prompt_delete_data_user_declines(self, mock_input):
        self.assertFalse(_prompt_delete_data("data.pickle"))

