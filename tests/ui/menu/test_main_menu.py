import unittest
from unittest.mock import patch

from mastermind.ui.menu.main_menu import MainMenu


class TestMainMenu(unittest.TestCase):
    @patch("builtins.input", return_value="1")
    @patch.object(MainMenu, "_process_option")
    def test_get_option_valid_input(self, mock_process_option, mock_input):
        menu = MainMenu()
        mock_process_option.return_value = "processed_option"
        self.assertEqual(menu.get_option(), "processed_option")
        mock_input.assert_called_once_with("Select an option: ")
        mock_process_option.assert_called_once_with("1")

    def test_process_option(self):
        menu = MainMenu()
        self.assertEqual(menu._process_option("1"), "Start New Game")
        self.assertEqual(menu._process_option("2"), "Load Saved Game")
        self.assertEqual(menu._process_option("3"), "Game History")
        self.assertEqual(menu._process_option("0"), "Save and Exit")
