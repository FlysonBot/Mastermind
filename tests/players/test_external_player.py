import unittest
from io import StringIO
from unittest.mock import patch

from src.game.game import Game
from src.players.external_player import ExternalCodeSetter


class TestExternalCodeSetter(unittest.TestCase):
    def setUp(self):
        self.game = Game(6, 4, 10, "HvAI")
        self.code_setter = ExternalCodeSetter(self.game._player_logic)

    def test_set_secret_code(self):
        self.code_setter.set_secret_code()
        self.assertFalse(hasattr(self.code_setter, "SECRET_CODE"))

    @patch("src.players.external_player.input")
    def test_get_valid_feedback(self, mock_input):
        mock_input.side_effect = ["2,1"]
        self.assertEqual(self.code_setter.get_feedback((1, 2, 3, 4)), (2, 1))

    @patch("src.players.external_player.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_get_invalid_feedback_wrong_format(self, mock_stdout, mock_input):
        mock_input.side_effect = ["2 1", "2,,1", "12"]
        self.code_setter.get_feedback((1, 2, 3, 4))
        self.assertIn("Invalid input format", mock_stdout.getvalue())

    @patch("src.players.external_player.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_get_invalid_feedback_out_of_range(self, mock_stdout, mock_input):
        mock_input.side_effect = ["5,1", "2,1"]
        self.code_setter.get_feedback((1, 2, 3, 4))
        self.assertIn(
            "Feedback must consist of 2 integer in range [0, 4)", mock_stdout.getvalue()
        )

    @patch("src.players.external_player.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_help(self, mock_stdout, mock_input):
        mock_input.side_effect = ["?", "12"]
        self.code_setter.get_feedback((1, 2, 3, 4))
        self.assertIn(
            "Enter a 2 digit number (optionally separated by comma) between 0 and 4.",
            mock_stdout.getvalue(),
        )

    @patch("src.players.external_player.input")
    def test_discard_game(self, mock_input):
        mock_input.side_effect = ["d"]
        self.assertEqual(self.code_setter.get_feedback((1, 2, 3, 4)), "d")

    @patch("src.players.external_player.input")
    def test_quit_game(self, mock_input):
        mock_input.side_effect = ["q"]
        self.assertEqual(self.code_setter.get_feedback((1, 2, 3, 4)), "q")

    @patch("src.players.external_player.input")
    def test_undo(self, mock_input):
        mock_input.side_effect = ["u"]
        self.assertEqual(self.code_setter.get_feedback((1, 2, 3, 4)), "u")


if __name__ == "__main__":
    unittest.main()
