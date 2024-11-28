import unittest
from unittest.mock import MagicMock, patch

from mastermind.game.game import Game
from mastermind.players.abstract_player import CodeCracker, CodeSetter, Player
from mastermind.utils import Stack


class TestPlayer(unittest.TestCase):
    class ConcretePlayer(Player):
        def undo(self, item: tuple) -> None:
            return super().undo(item)

    def setUp(self):
        # Create a mock for the Game class
        self.game = Game(6, 4, 10, "HvH")
        self.player = self.ConcretePlayer(self.game._player_logic)

    def test_init(self):
        self.assertEqual(self.player.game_state, self.game._state)
        self.assertIsInstance(self.player.undo_stack, Stack)

    @patch("mastermind.game.board.GameBoard.__len__", return_value=1)
    def test_undo(self, mock_len):
        self.player.undo((1, 2, 3, 4))
        self.assertEqual(self.player.undo_stack.pop(), (1, 2, 3, 4))

    def test_undo_from_empty_board(self):
        with self.assertRaises(self.game._board.EmptyBoardError):
            self.player.undo((1, 2, 3, 4))

    def test_redo(self):
        self.player.undo_stack.push((1, 2, 3, 4))
        self.assertEqual(self.player.redo(), (1, 2, 3, 4))
        self.assertEqual(len(self.player.undo_stack), 0)

    def test_redo_from_empty_stack(self):
        with self.assertRaises(IndexError):
            self.player.redo()

    def test_clear_undo(self):
        self.player.undo_stack.push((1, 2, 3, 4))
        self.player.undo_stack.push((5, 4, 3, 2))
        self.player.clear_undo()
        self.assertEqual(len(self.player.undo_stack), 0)


class TestCodeSetter(unittest.TestCase):
    class ConcreteCodeSetter(CodeSetter):
        set_secret_code = lambda: None  # noqa: E731
        get_feedback = lambda: None  # noqa: E731

    def setUp(self):
        self.game = Game(6, 4, 10, "HvH")
        self.code_setter = self.ConcreteCodeSetter(self.game._player_logic)

    @patch.object(ConcreteCodeSetter, "set_secret_code")
    @patch.object(ConcreteCodeSetter, "get_feedback")
    def test_undo(self, mock_get_feedback, mock_set_secret_code):
        self.code_setter.game_state._board._number_of_guesses_made = 1
        self.game._board.last_feedback = MagicMock(return_value=(2, 1, 0, 1))
        self.code_setter.undo()
        self.assertEqual(self.code_setter.undo_stack.pop(), (2, 1, 0, 1))
        self.assertFalse(mock_set_secret_code.called)
        self.assertFalse(mock_get_feedback.called)


class TestCodeCracker(unittest.TestCase):
    class ConcreteCodeCracker(CodeCracker):
        obtain_guess = lambda: None  # noqa: E731

    def setUp(self):
        self.game = Game(6, 4, 10, "HvH")
        self.win_msg = "You win in {step} steps!"
        self.lose_msg = "You lose after {step} steps."
        self.code_cracker = self.ConcreteCodeCracker(
            self.game._player_logic, self.win_msg, self.lose_msg
        )

    @patch.object(ConcreteCodeCracker, "obtain_guess")
    def test_undo(self, mock_obtain_guess):
        self.game._board._number_of_guesses_made = 1
        self.game._board.last_guess = MagicMock(return_value=(1, 2, 3, 4))
        self.code_cracker.undo()
        self.assertEqual(self.code_cracker.undo_stack.pop(), (1, 2, 3, 4))
        self.assertFalse(mock_obtain_guess.called)

    def test_win_message(self):
        self.game._board._number_of_guesses_made = 10
        with patch("builtins.print") as mock_print:
            self.code_cracker.win_message()
            mock_print.assert_called_with("You win in 10 steps!")

    def test_lose_message(self):
        self.game._board._number_of_guesses_made = 10
        with patch("builtins.print") as mock_print:
            self.code_cracker.lose_message()
            mock_print.assert_called_with("You lose after 10 steps.")


if __name__ == "__main__":
    unittest.main()
