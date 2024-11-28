import unittest
from io import StringIO
from unittest.mock import patch

from src.game.game import Game
from src.players.human_player import HumanCodeCracker, HumanCodeSetter


class TestHumanCodeSetter(unittest.TestCase):
    def setUp(self):
        self.game = Game(6, 4, 10, "HvH")
        self.human_code_setter = HumanCodeSetter(self.game._player_logic)

    @patch("src.players.human_player.getpass")
    def test_set_secret_code(self, mock_getpass):
        mock_getpass.side_effect = ["1234", "1234"]
        self.human_code_setter.set_secret_code()
        self.assertEqual(self.human_code_setter.SECRET_CODE, (1, 2, 3, 4))

    @patch("src.players.human_player.getpass")
    @patch("sys.stdout", new_callable=StringIO)
    def test_set_secret_code_invalid_input(self, mock_stdout, mock_getpass):
        mock_getpass.side_effect = ["123a", "1234", "1235", "1235", "1235"]
        self.human_code_setter.set_secret_code()
        self.assertIn("Invalid input format", mock_stdout.getvalue())
        self.assertIn("To get more help, enter '?'", mock_stdout.getvalue())
        self.assertIn("Code does not match. Try again.", mock_stdout.getvalue())

    @patch("src.players.human_player.getpass")
    @patch("sys.stdout", new_callable=StringIO)
    def test_set_secret_code_out_of_range(self, mock_stdout, mock_getpass):
        mock_getpass.side_effect = ["1237", "1234", "1234"]
        self.human_code_setter.set_secret_code()
        self.assertIn(
            "Guess must consist of 4 integers in range [1, 6]", mock_stdout.getvalue()
        )
        self.assertIn("To get more help, enter '?'", mock_stdout.getvalue())

    @patch("src.players.human_player.getpass")
    @patch("sys.stdout", new_callable=StringIO)
    def test_set_secret_code_help(self, mock_stdout, mock_getpass):
        mock_getpass.side_effect = ["?", "1234", "1234"]
        self.human_code_setter.set_secret_code()
        self.assertIn(
            "Enter a 4-digit number with digit ranging from 1 to 6",
            mock_stdout.getvalue(),
        )
        self.assertIn(
            "For example, a 6-digit 4-color code can be 123412, or 1,2,3,4,1,2",
            mock_stdout.getvalue(),
        )
        self.assertIn("Or, you can enter a command:", mock_stdout.getvalue())
        self.assertIn("(?) for help", mock_stdout.getvalue())
        self.assertIn("(d) to discard the game", mock_stdout.getvalue())

    @patch("src.players.human_player.getpass")
    def test_set_secret_code_discard_game(self, mock_getpass):
        mock_getpass.return_value = "d"
        self.assertEqual(self.human_code_setter.set_secret_code(), "d")

    def test_get_feedback(self):
        self.human_code_setter.SECRET_CODE = (1, 2, 3, 4)
        feedback = self.human_code_setter.get_feedback((1, 2, 5, 4))
        self.assertEqual(feedback, (3, 0))

    def test_get_feedback_without_secret_code(self):
        with self.assertRaises(NotImplementedError):
            self.human_code_setter.get_feedback((1, 2, 3, 4))


class TestHumanCodeCracker(unittest.TestCase):
    def setUp(self):
        self.game = Game(6, 4, 10, "HvH")
        self.human_code_cracker = HumanCodeCracker(self.game._player_logic)

    @patch("builtins.input")
    def test_obtain_guess(self, mock_input):
        mock_input.return_value = "1234"
        guess = self.human_code_cracker.obtain_guess()
        self.assertEqual(guess, (1, 2, 3, 4))

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_obtain_guess_invalid_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ["123a", "?", "1234"]
        self.human_code_cracker.obtain_guess()
        self.assertIn("To get more help, enter '?'", mock_stdout.getvalue())

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_obtain_guess_out_of_range(self, mock_stdout, mock_input):
        mock_input.side_effect = ["1237", "?", "1234"]
        self.human_code_cracker.obtain_guess()
        self.assertIn("To get more help, enter '?'", mock_stdout.getvalue())

    @patch("builtins.input")
    def test_obtain_guess_discard_game(self, mock_input):
        mock_input.return_value = "d"
        self.assertEqual(self.human_code_cracker.obtain_guess(), "d")

    @patch("builtins.input")
    def test_obtain_guess_quit_game(self, mock_input):
        mock_input.return_value = "q"
        self.assertEqual(self.human_code_cracker.obtain_guess(), "q")

    @patch("builtins.input")
    def test_obtain_guess_undo(self, mock_input):
        mock_input.return_value = "u"
        self.assertEqual(self.human_code_cracker.obtain_guess(), "u")

    @patch("builtins.input")
    def test_obtain_guess_redo(self, mock_input):
        mock_input.return_value = "r"
        self.assertEqual(self.human_code_cracker.obtain_guess(), "r")


if __name__ == "__main__":
    unittest.main()
