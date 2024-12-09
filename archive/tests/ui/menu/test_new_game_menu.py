import unittest
from unittest.mock import call, patch

from mastermind.ui.menu.new_game_menu import NewGameMenu


class TestNewGameMenu(unittest.TestCase):
    def setUp(self):
        self.menu = NewGameMenu()

    def test_name(self):
        self.assertEqual(self.menu.name, "New Game Menu")

    @patch("builtins.input", return_value="2")
    @patch.object(NewGameMenu, "_process_option")
    def test_get_option_valid_input(self, mock_process_option, mock_input):
        mock_process_option.return_value = "processed_option"
        self.assertEqual(self.menu.get_option(), "processed_option")
        mock_input.assert_called_once_with("Select an option: ")
        mock_process_option.assert_called_once_with("2")

    @patch("builtins.input", side_effect=["invalid", "0"])
    @patch.object(NewGameMenu, "display")
    def test_get_option_invalid_input(self, mock_display, mock_input):
        self.assertEqual(self.menu.get_option(), "Return to Main Menu")
        mock_input.assert_has_calls(
            [call("Select an option: "), call("Select an option: ")]
        )
        self.assertEqual(mock_display.call_count, 2)

    def test_process_option(self):
        self.assertEqual(self.menu._process_option("1"), "You vs Someone Else")
        self.assertEqual(self.menu._process_option("2"), "You vs AI")
        self.assertEqual(self.menu._process_option("3"), "AI vs You")
        self.assertEqual(self.menu._process_option("4"), "Solve External Game")
        self.assertEqual(self.menu._process_option("0"), "Return to Main Menu")
