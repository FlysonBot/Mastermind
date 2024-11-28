import unittest
from unittest.mock import patch

from mastermind.game.game import Game
from mastermind.game.game_flow import GameFlow
from mastermind.game.player_logic import PlayerLogic


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(6, 4, 10, "HvH")

    def test_init(self):
        self.assertEqual(self.game._state.number_of_colors, 6)
        self.assertEqual(self.game._state.number_of_dots, 4)
        self.assertEqual(self.game._state.MAXIMUM_ATTEMPTS, 10)
        self.assertEqual(self.game._state.GAME_MODE, "HvH")
        self.assertIsInstance(self.game._player_logic, PlayerLogic)
        self.assertIsInstance(self.game._game_flow, GameFlow)

    def test_cross_reference(self):
        self.assertIs(self.game._board, self.game._state._board)
        self.assertIs(self.game._player_logic.game_state, self.game._state)
        self.assertIs(self.game._game_flow.game_state, self.game._state)
        self.assertIs(self.game._game_flow.player_logic, self.game._player_logic)

    def test_properties(self):
        self.assertEqual(self.game.number_of_colors, 6)
        self.assertEqual(self.game.number_of_dots, 4)
        self.assertEqual(self.game.maximum_attempts, 10)
        self.assertEqual(self.game.game_mode, "HvH")

    @patch.object(GameFlow, "start_game")
    def test_start_game(self, mock_start_game):
        mock_start_game.return_value = "q"
        self.assertEqual(self.game.start_game(), "q")
        mock_start_game.assert_called()

    @patch.object(GameFlow, "resume_game")
    def test_resume_game(self, mock_resume_game):
        mock_resume_game.return_value = "q"
        self.assertEqual(self.game.resume_game(), "q")
        mock_resume_game.assert_called()

    def test_len(self):
        self.game._board.add_guess((1, 2, 3, 4), (1, 2))
        self.assertEqual(len(self.game), 1)


if __name__ == "__main__":
    unittest.main()
