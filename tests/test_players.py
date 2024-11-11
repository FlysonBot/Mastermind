from getpass import getpass
import unittest
from unittest.mock import MagicMock, patch

from mastermind.gameboard import Game
from mastermind.players import Player, CodeSetter, CodeCracker, HumanSetter, AISetter, ExternalSetter, HumanCracker, AICracker
from mastermind.utils import Stack, get_feedback
from mastermind.validation import ValidGuess, ValidFeedback


class TestPlayers(unittest.TestCase):
    
    def setUp(self):
        """Initialize a basic Game instance for testing purposes."""
        self.game = Game(number_of_colors=6, number_of_dots=4, maximum_attempts=10, game_mode="HvH")

    # Tests for HumanSetter
    @patch("getpass", return_value="1234")
    def test_human_setter_set_secret_code_valid(self, mock_getpass):
        """Test HumanSetter setting a valid secret code."""
        setter = HumanSetter(self.game)
        self.assertIsNone(setter.set_secret_code())
        self.assertEqual(setter.SECRET_CODE, (1, 2, 3, 4))

    @patch("getpass", side_effect=["?", "1234", "1234"])
    def test_human_setter_help_command(self, mock_getpass):
        """Test HumanSetter help command (?) during code entry."""
        setter = HumanSetter(self.game)
        with patch("builtins.print") as mock_print:
            setter.set_secret_code()
            print_log = str(mock_print.call_args_list)
            
            self.assertIn("Enter a 4-digit number with digit ranging from 1 to 6", print_log)

    def test_human_setter_get_feedback_no_code(self):
        """Test get_feedback raises error if secret code isn't set."""
        setter = HumanSetter(self.game)
        with self.assertRaises(NotImplementedError):
            setter.get_feedback((1, 2, 3, 4))

    # Tests for AISetter
    def test_ai_setter_set_secret_code(self):
        """Test AISetter's random code generation."""
        setter = AISetter(self.game)
        setter.set_secret_code()
        self.assertEqual(len(setter.SECRET_CODE), self.game.number_of_dots)
        self.assertTrue(all(1 <= digit <= self.game.number_of_colors for digit in setter.SECRET_CODE))

    def test_ai_setter_get_feedback(self):
        """Test AISetter feedback generation."""
        setter = AISetter(self.game)
        setter.SECRET_CODE = (1, 2, 3, 4)
        feedback = setter.get_feedback((1, 2, 3, 4))
        self.assertEqual(feedback, (4, 0))  # all correct positions and colors

    # Tests for ExternalSetter
    @patch("builtins.input", side_effect=["m", "?", "90", "01", "0,1", "q", "d"])
    def test_external_setter_get_feedback(self, mock_input):
        """Test ExternalSetter feedback input with commands."""
        setter = ExternalSetter(self.game)
        with patch("builtins.print") as mock_print:
            feedback = setter.get_feedback((1, 2, 3, 4))
            print_log = str(mock_print.call_args_list)
            
            self.assertIn("To get more help, enter '?'", print_log)
            self.assertIn("Enter a 2 digit number", print_log)
            self.assertIn("(?) for help", print_log)
            self.assertIn("Feedback must consist of 2 integer in range", print_log)
            
            self.assertEqual(feedback, (0, 1))
            self.assertEqual(setter.get_feedback((1, 2, 3, 4)), (0,1))
            self.assertEqual(setter.get_feedback((1, 2, 3, 4)), "q")
            self.assertEqual(setter.get_feedback((1, 2, 3, 4)), "d")

    # Tests for HumanCracker
    @patch("builtins.input", side_effect=["m", "?", "12", "1239", "1234", "u", "d"])
    def test_human_cracker_obtain_guess(self, mock_input):
        """Test HumanCracker obtaining guesses and commands."""
        cracker = HumanCracker(self.game)
        with patch("builtins.print") as mock_print:
            valid_guess = cracker.obtain_guess()
            print_log = str(mock_print.call_args_list)
            
            self.assertIn("To get more help, enter '?'", str(mock_print.call_args_list[1]))
            self.assertIn("Enter a 4-digit", print_log)
            self.assertIn("Guess must consist of 4 integers in range [1, 6]", print_log)
            
            #self.assertEqual(valid_guess, (1, 2, 3, 4))
            self.assertEqual(cracker.obtain_guess(), "u")
            self.assertEqual(cracker.obtain_guess(), "d")

    @patch("builtins.print")
    def test_human_cracker_win_message(self, mock_print):
        """Test HumanCracker's win message output."""
        cracker = HumanCracker(self.game)
        cracker.win_message()
        mock_print.assert_called_once_with("Congratulations! You won in 0 steps!")

    # Tests for undo and redo functionality
    def test_undo_with_guesses(self):
        """Test undo functionality with multiple undos."""
        cracker = HumanCracker(self.game)
        setter = HumanSetter(self.game)
        self.game._board.add_guess((1, 2, 3, 4), (1, 1))
        self.game._board.add_guess((2, 3, 4, 1), (1, 0))
        self.game._board.add_guess((2, 3, 4, 4), (1, 1))
        self.game._board.add_guess((2, 4, 4, 4), (1, 2))
        for _ in range(3):
            cracker.undo()
            setter.undo()
            self.game._board.remove_last()
        self.assertEqual(cracker.undo_stack[0], (2, 3, 4, 1))
        self.assertEqual(cracker.undo_stack[1], (2, 3, 4, 4))
        self.assertEqual(cracker.undo_stack[2], (2, 4, 4, 4))
        self.assertEqual(setter.undo_stack[0], (1, 0))
        self.assertEqual(setter.undo_stack[1], (1, 1))
        self.assertEqual(setter.undo_stack[2], (1, 2))
        self.assertEqual(len(cracker.undo_stack), 3)
        self.assertEqual(len(setter.undo_stack), 3)
    
    def test_redo_with_undone_guess(self):
        """Test redo functionality after undo to confirm guesses are actually being redo."""
        cracker = HumanCracker(self.game)
        setter = HumanSetter(self.game)
        self.game._board.add_guess((1, 2, 3, 4), (1, 1))
        self.game._board.add_guess((2, 3, 4, 1), (1, 0))
        self.game._board.add_guess((2, 3, 4, 4), (1, 1))
        self.game._board.add_guess((2, 4, 4, 4), (1, 2))
        for _ in range(3):
            cracker.undo()
            setter.undo()
            self.game._board.remove_last()
        cracker.redo()
        setter.redo()
        self.assertEqual(cracker.undo_stack[0], (2, 3, 4, 4))
        self.assertEqual(cracker.undo_stack[1], (2, 4, 4, 4))
        self.assertEqual(setter.undo_stack[0], (1, 1))
        self.assertEqual(setter.undo_stack[1], (1, 2))
        self.assertEqual(len(cracker.undo_stack), 2)
        self.assertEqual(len(setter.undo_stack), 2)
        cracker.redo()
        setter.redo()
        self.assertEqual(cracker.undo_stack[0], (2, 4, 4, 4))
        self.assertEqual(setter.undo_stack[0], (1, 2))
        self.assertEqual(len(cracker.undo_stack), 1)
        self.assertEqual(len(setter.undo_stack), 1)
        cracker.redo()
        setter.redo()
        self.assertEqual(len(cracker.undo_stack), 0)
        self.assertEqual(len(setter.undo_stack), 0)

    def test_redo_no_action_when_stack_empty(self):
        """Test redo raise error without an undo first."""
        cracker = HumanCracker(self.game)
        setter = HumanSetter(self.game)

        self.game._board.add_guess((1, 2, 3, 4), (1, 1))
        self.game._board.add_guess((2, 3, 4, 1), (1, 0))
        with self.assertRaises(IndexError):
            cracker.redo()
    
    def test_undo_stack_cleared_after_new_guess(self):
        """Test undo stack is being cleared after submitting a new guess."""
        self.game._game_started = True
        self.game.find_players()
        cracker = self.game.PLAYER_CRACKER
        setter = self.game.PLAYER_SETTER
        self.game.submit_guess((1, 2, 3, 4), (1, 1))
        self.game.submit_guess((2, 3, 4, 1), (1, 0))
        cracker.undo()
        setter.undo()
        self.assertEqual(len(cracker.undo_stack), 1)
        self.assertEqual(len(setter.undo_stack), 1)
        
        self.game.submit_guess((1, 2, 3, 4), (1, 1))
        self.assertEqual(len(cracker.undo_stack), 0)
        self.assertEqual(len(setter.undo_stack), 0)

# Run the tests
if __name__ == '__main__':
    unittest.main()
