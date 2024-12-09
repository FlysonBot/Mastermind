import unittest
from unittest.mock import patch

from mastermind.ui.menu.resume_game_menu import ResumeGameMenu, _is_option_valid


class TestResumeGameMenu(unittest.TestCase):
    """Unit tests for the ResumeGameMenu class"""

    def setUp(self):
        """Set up the test environment"""
        self.example_continuable_games = [
            {
                "game_mode": "HvH",
                "number_of_dots": 4,
                "number_of_colors": 6,
                "amount_attempted": 8,
                "amount_allowed": 10,
                "win_status": None,
                "guesses": ["1234", "4561"],
                "feedback": [(4, 0), (3, 1)],
            },
            {
                "game_mode": "HvAI",
                "number_of_dots": 5,
                "number_of_colors": 8,
                "amount_attempted": 10,
                "amount_allowed": 12,
                "win_status": None,
                "guesses": ["1234", "4561", "2312"],
                "feedback": [(4, 0), (3, 1), (2, 2)],
            },
        ]

    def test_init(self):
        """Test the initialization of the ResumeGameMenu"""
        menu = ResumeGameMenu()
        self.assertEqual(menu.name, "Resume Game")
        self.assertEqual(menu.width, 27)
        self.assertEqual(menu._empty_message, "No continuable game found.")
        self.assertEqual(menu.menu, {"0": "Return to Main Menu"})

    @patch("mastermind.main.game_history.list_continuable_games")
    def test_fetch_data_with_games(self, mock_continuable_games):
        """Test the _fetch_data method with continuable games"""
        mock_continuable_games.return_value = self.example_continuable_games
        menu = ResumeGameMenu()
        data = menu._fetch_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(menu.menu_length, 2)

    @patch("mastermind.main.game_history.GameHistoryManager.retrieve_continuable_games")
    def test_fetch_data_without_games(self, mock_retrieve_games):
        """Test the _fetch_data method with no continuable games"""
        mock_retrieve_games.return_value = None
        menu = ResumeGameMenu()
        data = menu._fetch_data()
        self.assertIsNone(data)
        self.assertEqual(menu.menu_length, 0)

    @patch("builtins.print")
    @patch("mastermind.main.game_history.list_continuable_games")
    def test_render_data(self, mock_continuable_games, mock_print):
        """Test the _render_data method"""
        mock_continuable_games.return_value = self.example_continuable_games
        menu = ResumeGameMenu()
        data = menu._fetch_data()
        menu._render_data(data)

        mock_print.assert_any_call("    Mode Dimension Attempts")
        mock_print.assert_any_call("(1) HvH  6x4         8/10  ")
        mock_print.assert_any_call("(2) HvAI 8x5         10/12 ")
        mock_print.assert_any_call("\n(0) Return to Main Menu")

    def test_process_option_return(self):  # sourcery skip: class-extract-method
        """Test the _process_option method when the user selects 'Return to Main Menu'"""
        menu = ResumeGameMenu()
        result = menu._process_option("0")
        self.assertEqual(result, "return")

    def test_process_option_select_game(self):
        """Test the _process_option method when the user selects a game to resume"""
        menu = ResumeGameMenu()
        result = menu._process_option("2")
        self.assertEqual(result, 1)

    def test_is_option_valid_valid_input(self):
        """Test the _is_option_valid function with valid input"""
        self.assertTrue(_is_option_valid("2", 3))

    def test_is_option_valid_invalid_input(self):
        """Test the _is_option_valid function with invalid input"""
        self.assertFalse(_is_option_valid("a", 3))
        self.assertFalse(_is_option_valid("4", 3))

    @patch("builtins.input", side_effect=[""])
    @patch("mastermind.main.game_history.GameHistoryManager.retrieve_continuable_games")
    @patch("builtins.print")
    def test_get_option_without_games(
        self, mock_print, mock_retrieve_games, mock_input
    ):
        """Test the get_option method with no continuable games"""
        mock_retrieve_games.return_value = None
        menu = ResumeGameMenu()
        result = menu.get_option()
        self.assertEqual(result, 0)
        self.assertEqual(mock_print.call_count, 3)
        mock_print.assert_any_call("No continuable game found.")

    @patch("builtins.input", side_effect=["9", "a", "2"])
    @patch("mastermind.main.game_history.list_continuable_games")
    @patch("mastermind.ui.menu.resume_game_menu.ResumeGameMenu._render_data")
    def test_get_option_with_games(
        self, mock_render_data, mock_continuable_games, mock_input
    ):
        """Test the get_option method with continuable games"""
        mock_continuable_games.return_value = self.example_continuable_games
        menu = ResumeGameMenu()
        result = menu.get_option()
        self.assertEqual(result, 2)
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(mock_render_data.call_count, 3)
