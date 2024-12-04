import unittest
from unittest.mock import create_autospec, patch

from mastermind.main.game_storage import (
    list_continuable_games,
    list_continuable_games_index,
    retrieve_stored_games,
)
from mastermind.storage.user_data import UserDataManager


class TestMastermindStorage(unittest.TestCase):
    """Unit tests for the mastermind.storage module"""

    def setUp(self):
        self.sample_games = [
            {"game_id": 1, "win_status": None},
            {"game_id": 2, "win_status": True},
            {"game_id": 3, "win_status": False},
            {"game_id": 4, "win_status": None},
        ]  # Note: For testing only! Actual data doesn't looks like this!

    def test_retrieve_stored_games(self):
        """Test the retrieve_stored_games function"""
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = self.sample_games

        with patch("mastermind.main.game_storage.userdata", new=mock_user_data_manager):
            games = retrieve_stored_games()
            self.assertEqual(games, self.sample_games)

    def test_retrieve_empty_games(self):
        """Test the retrieve_stored_games function"""
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = []

        with patch("mastermind.main.game_storage.userdata", new=mock_user_data_manager):
            games = retrieve_stored_games()
        self.assertEqual(games, [])

    def test_list_continuable_games_index(self):
        """Test the list_continuable_games_index function"""
        continuable_indexes = list_continuable_games_index(self.sample_games)
        self.assertEqual(continuable_indexes, [0, 3])

        continuable_indexes = list_continuable_games_index([])
        self.assertEqual(continuable_indexes, [])

    def test_list_continuable_games(self):
        """Test the list_continuable_games function"""
        continuable_games = list_continuable_games(self.sample_games)
        self.assertEqual(
            continuable_games, [self.sample_games[0], self.sample_games[3]]
        )

        continuable_games = list_continuable_games([])
        self.assertEqual(continuable_games, [])


if __name__ == "__main__":
    unittest.main()
