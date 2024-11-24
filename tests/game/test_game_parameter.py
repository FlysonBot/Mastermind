import unittest
from unittest.mock import patch

from src.game.board import GameBoard
from src.game.game_parameter import GameParameter


class TestGameParameter(unittest.TestCase):
    def setUp(self):
        self.game_param = GameParameter(6, 4, 10, "HvH")

    def test_init(self):
        self.assertEqual(self.game_param.MAXIMUM_ATTEMPTS, 10)
        self.assertEqual(self.game_param.GAME_MODE, "HvH")
        self.assertIsInstance(self.game_param._board, GameBoard)
        self.assertFalse(self.game_param.game_started)
        self.assertIsNone(self.game_param.win_status)

    def test_number_of_colors_and_dots(self):
        self.assertEqual(self.game_param.number_of_colors, 6)
        self.assertEqual(self.game_param.number_of_dots, 4)

    def test_len(self):
        self.assertEqual(len(self.game_param), 0)
        self.game_param._board.add_guess((1, 2, 3, 4), (2, 1))
        self.assertEqual(len(self.game_param), 1)

    def test_check_and_update_win_status_win(self):
        self.assertIsNone(self.game_param.win_status)
        self.game_param.SECRET_CODE = (1, 2, 3, 4)
        self._guess_and_check_win_status_with_feedback((0, 0))

    def test_check_and_update_win_status_win_on_perfect_feedback(self):
        self.assertIsNone(self.game_param.win_status)
        self._guess_and_check_win_status_with_feedback((4, 0))

    def _guess_and_check_win_status_with_feedback(self, feedback: tuple):
        self.game_param._board.add_guess((1, 2, 3, 4), feedback)
        self.assertTrue(self.game_param.check_and_update_win_status())
        self.assertTrue(self.game_param.win_status)

    def test_check_and_update_win_status_loss(self):
        self.assertIsNone(self.game_param.win_status)
        self.game_param.MAXIMUM_ATTEMPTS = 1
        self.game_param._board.add_guess((1, 2, 3, 4), (2, 1))
        self.assertFalse(self.game_param.check_and_update_win_status())
        self.assertFalse(self.game_param.win_status)
    
    def test_check_and_update_win_status_continue(self):
        self.assertIsNone(self.game_param.win_status)
        self.game_param._board.add_guess((1, 2, 3, 4), (2, 1))
        self.assertIsNone(self.game_param.check_and_update_win_status())
        self.assertIsNone(self.game_param.win_status)

    @patch.object(GameParameter, "_last_guess_is_secret", return_value=False)
    @patch.object(GameParameter, "_last_feedback_is_perfect", return_value=False)
    @patch.object(GameParameter, "_reached_maximum_attempts", return_value=False)
    def test_check_and_update_win_status_in_progress(
        self,
        mock_last_guess_is_secret,
        mock_last_feedback_is_perfect,
        mock_reached_maximum_attempts,
    ):
        self.assertIsNone(self.game_param.win_status)
        self.assertIsNone(self.game_param.check_and_update_win_status())
        self.assertIsNone(self.game_param.win_status)


if __name__ == "__main__":
    unittest.main()
