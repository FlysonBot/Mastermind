import unittest
from io import StringIO
from unittest.mock import call, create_autospec, patch

from mastermind.game.game import Game
from mastermind.main.game_controller import GameController
from mastermind.storage.user_data import UserDataManager


class TestGameController(unittest.TestCase):
    """Unit tests for the GameController class"""

    @patch("builtins.input", side_effect=["6", "4", "10", "q"])
    @patch("mastermind.main.game_controller.GameHistoryManager.save_game")
    def test_start_new_game_classic(self, mock_save_game, mock_input):
        """Test starting a new Classic game"""
        with patch("sys.stdout", new=StringIO()):
            GameController.start_new_game("HvAI")

        mock_input.assert_has_calls(
            [
                call("\nEnter the number of colors (2-10): "),
                call("\nEnter the number of dots (2-10): "),
                call("\nEnter the maximum number of attempts: "),
            ]
        )
        mock_save_game.assert_called_once()

    @patch("builtins.input", side_effect=["8", "5", "15", "q"])
    @patch("mastermind.main.game_controller.GameHistoryManager.save_game")
    def test_start_new_game_custom(self, mock_save_game, mock_input):
        """Test starting a new Custom game"""
        with patch("sys.stdout", new=StringIO()):
            GameController.start_new_game("HvAI")

        mock_input.assert_has_calls(
            [
                call("\nEnter the number of colors (2-10): "),
                call("\nEnter the number of dots (2-10): "),
                call("\nEnter the maximum number of attempts: "),
            ]
        )
        mock_save_game.assert_called_once()

    def test_resume_game_discard(self):
        """Test resuming a game and discarding it"""
        game_mock = create_autospec(Game, instance=True)
        game_mock.resume_game.return_value = "d"
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = [
            {
                "game": game_mock,
                "game_mode": "HvH",
                "number_of_dots": 4,
                "number_of_colors": 6,
                "amount_attempted": 8,
                "amount_allowed": 10,
                "win_status": None,
                "guesses": ["1234", "4561", "2312"],
                "feedback": [(4, 0), (3, 1), (2, 2)],
            }
        ]

        with patch(
            "mastermind.main.game_controller.userdata",
            new=mock_user_data_manager,
        ):
            GameController.resume_game(0)

        self.assertEqual(mock_user_data_manager.saved_games, [])

    @patch("builtins.input", side_effect=["q"])
    def test_resume_game_update_saved(self, mock_input):
        """Test resuming a game and updating the saved game"""
        game = Game(6, 4, 10, "HvAI")
        game._state.game_started = True
        game._player_logic.initialize_players()

        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.saved_games = [
            {
                "game": game,
                "game_mode": "HvAI",
                "number_of_dots": 4,
                "number_of_colors": 6,
                "amount_attempted": 3,
                "amount_allowed": 10,
                "win_status": None,
                "guesses": ["1234", "4561", "2312"],
                "feedback": [(4, 0), (3, 1), (2, 2)],
            }
        ]

        with patch(
            "mastermind.main.game_controller.userdata", new=mock_user_data_manager
        ):
            with patch("sys.stdout", new=StringIO()):
                GameController.resume_game(0)

            self.assertEqual(len(mock_user_data_manager.saved_games), 1)
            self.assertIsNone(mock_user_data_manager.saved_games[0]["win_status"])


if __name__ == "__main__":
    unittest.main()
