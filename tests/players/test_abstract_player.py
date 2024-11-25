import unittest
from unittest.mock import MagicMock, patch

from src.game.board import GameBoard
from src.game.game import Game
from src.players.abstract_player import CodeCracker, CodeSetter, Player
from src.utils import Stack


class TestPlayer(unittest.TestCase):
    class ConcretePlayer(Player):
        def undo(self, item: tuple) -> None:
            return super().undo(item)

    def setUp(self):
        self.game = MagicMock(spec=Game)
        self.game._board = MagicMock(spec=GameBoard)
        self.player = self.ConcretePlayer(self.game)

    def test_init(self):
        self.assertEqual(self.player.game_state, self.game)
        self.assertIsInstance(self.player.undo_stack, Stack)

    def test_undo(self):
        self.game._board.__len__.return_value = 1
        self.player.undo((1, 2, 3, 4))
        self.assertEqual(self.player.undo_stack.pop(), (1, 2, 3, 4))

    def test_undo_from_empty_board(self):
        self.game._board.EmptyBoardError = Exception
        self.game._board.last_feedback.side_effect = self.game._board.EmptyBoardError
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
        self.game = MagicMock(spec=Game)
        self.game._board = MagicMock(spec=GameBoard)
        self.code_setter = self.ConcreteCodeSetter(self.game)

    @patch.object(ConcreteCodeSetter, "set_secret_code")
    @patch.object(ConcreteCodeSetter, "get_feedback")
    def test_undo(self, mock_get_feedback, mock_set_secret_code):
        self.game._board.__len__.return_value = 1
        self.game._board.last_feedback.return_value = (2, 1, 0, 1)
        self.code_setter.undo()
        self.assertEqual(self.code_setter.undo_stack.pop(), (2, 1, 0, 1))
        self.assertFalse(mock_set_secret_code.called)
        self.assertFalse(mock_get_feedback.called)


class TestCodeCracker(unittest.TestCase):
    class ConcreteCodeCracker(CodeCracker):
        obtain_guess = lambda: None  # noqa: E731

    def setUp(self):
        self.game = MagicMock(spec=Game)
        self.game._board = MagicMock(spec=GameBoard)
        self.win_msg = "You win in {step} steps!"
        self.lose_msg = "You lose after {step} steps."
        self.code_cracker = self.ConcreteCodeCracker(
            self.game, self.win_msg, self.lose_msg
        )

    @patch.object(ConcreteCodeCracker, "obtain_guess")
    def test_undo(self, mock_obtain_guess):
        self.game._board.__len__.return_value = 1
        self.game._board.last_guess.return_value = (1, 2, 3, 4)
        self.code_cracker.undo()
        self.assertEqual(self.code_cracker.undo_stack.pop(), (1, 2, 3, 4))
        self.assertFalse(mock_obtain_guess.called)

    def test_win_message(self):
        self.game.__len__.return_value = 10
        with patch("builtins.print") as mock_print:
            self.code_cracker.win_message()
            mock_print.assert_called_with("You win in 10 steps!")

    def test_lose_message(self):
        self.game.__len__.return_value = 10
        with patch("builtins.print") as mock_print:
            self.code_cracker.lose_message()
            mock_print.assert_called_with("You lose after 10 steps.")


if __name__ == "__main__":
    unittest.main()
