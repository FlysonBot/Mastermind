import unittest
from unittest.mock import create_autospec, patch

import pandas as pd

from mastermind.game.game import Game
from mastermind.main.game_history import GameHistoryManager, game_list_to_pandas
from mastermind.storage.user_data import UserDataManager


class TestGameHistoryManager(unittest.TestCase):
    """Unit tests for the GameHistoryManager class"""

    def setUp(self):
        self.sample_games = [
            {
                "game_mode": "HvH",
                "number_of_dots": 4,
                "number_of_colors": 6,
                "amount_attempted": 8,
                "amount_allowed": 10,
                "win_status": True,
                "guesses": ["1234", "4561", "2312"],
                "feedback": [(4, 0), (3, 1), (2, 2)],
            },
            {
                "game_mode": "HvAI",
                "number_of_dots": 5,
                "number_of_colors": 8,
                "amount_attempted": 12,
                "amount_allowed": 15,
                "win_status": False,
                "guesses": ["12345", "45612", "34567"],
                "feedback": [(3, 2), (2, 3), (0, 5)],
            },
            {
                "game_mode": "AIvH",
                "number_of_dots": 4,
                "number_of_colors": 6,
                "amount_attempted": 5,
                "amount_allowed": 10,
                "win_status": None,
                "guesses": ["1234", "4561"],
                "feedback": [(4, 0), (3, 1)],
            },
        ]

    def test_save_game(self):
        """Test the save_game method"""
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = []

        with patch("mastermind.main.game_history.userdata", new=mock_user_data_manager):
            self._set_up_game_and_test_saved(mock_user_data_manager)

    def test_save_game_with_empty_list(self):
        """Test the save_game method when the saved_games list is empty"""
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = None

        with patch("mastermind.main.game_history.userdata", new=mock_user_data_manager):
            self._set_up_game_and_test_saved(mock_user_data_manager)

    def _set_up_game_and_test_saved(self, mock_user_data_manager):
        game = Game(4, 6, 10, "HvH")
        game_metadata = GameHistoryManager.generate_meta_data(game)
        GameHistoryManager.save_game(game)
        self.assertIn(game_metadata, mock_user_data_manager.saved_games)

    def test_retrieve_game_history_with_no_games(self):
        """Test the retrieve_game_history method when there are no games"""
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = None

        with patch("mastermind.main.game_storage.userdata", new=mock_user_data_manager):
            game_history = GameHistoryManager.retrieve_game_history()
            self.assertIsNone(game_history)

    def test_retrieve_continuable_games_with_no_games(self):
        """Test the retrieve_continuable_games method when there are no games"""
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = None

        with patch("mastermind.main.game_storage.userdata", new=mock_user_data_manager):
            continuable_games = GameHistoryManager.retrieve_continuable_games()
            self.assertIsNone(continuable_games)

    @patch("mastermind.main.game_storage.retrieve_stored_games", return_value=None)
    def test_game_list_to_pandas_with_no_games(self, mock_retrieve_stored_games):
        """Test the game_list_to_pandas function when there are no games"""
        dataframe = game_list_to_pandas([])
        self.assertIsNone(dataframe)

    def test_game_list_to_pandas(self):
        """Test the game_list_to_pandas function"""
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = self.sample_games

        with patch("mastermind.main.game_history.userdata", new=mock_user_data_manager):
            dataframe = game_list_to_pandas(self.sample_games)
            self.assertIsInstance(dataframe, pd.DataFrame)
            self.assertEqual(len(dataframe), 3)
            self.assertListEqual(
                list(dataframe.columns), ["Mode", "Dimension", "Attempts"]
            )
            self.assertListEqual(list(dataframe["Mode"]), ["HvH", "HvAI", "AIvH"])
            self.assertListEqual(list(dataframe["Dimension"]), ["6x4", "8x5", "6x4"])
            self.assertListEqual(
                list(dataframe["Attempts"]), ["W 8/10", "L 12/15", "  5/10"]
            )


if __name__ == "__main__":
    unittest.main()
