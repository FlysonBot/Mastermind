import unittest
from src.game.board import GameBoard


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.board = GameBoard(6, 4)

    def test_init(self):
        self.assertEqual(self.board.NUMBER_OF_COLORS, 6)
        self.assertEqual(self.board.NUMBER_OF_DOTS, 4)
        self.assertEqual(len(self.board), 0)

    def test_get_item(self):
        self.board.add_guess((1, 2, 3, 4), (2, 1, 0, 1))
        self.board.add_guess((5, 4, 3, 2), (1, 2, 1, 0))
        self.assertEqual(self.board[0], ((5, 4, 3, 2), (1, 2, 1, 0)))
        self.assertEqual(self.board[1], ((1, 2, 3, 4), (2, 1, 0, 1)))

    def test_get_item_with_invalid_index(self):
        self.board.add_guess((1, 2, 3, 4), (2, 1, 0, 1))
        with self.assertRaises(IndexError):
            _ = self.board[1]

    def test_len(self):
        self.assertEqual(len(self.board), 0)
        self.board.add_guess((1, 2, 3, 4), (2, 1, 0, 1))
        self.assertEqual(len(self.board), 1)
        self.board.add_guess((5, 4, 3, 2), (1, 2, 1, 0))
        self.assertEqual(len(self.board), 2)

    def test_last_guess(self):
        self.board.add_guess((1, 2, 3, 4), (2, 1, 0, 1))
        self.board.add_guess((5, 4, 3, 2), (1, 2, 1, 0))
        self.assertEqual(self.board.last_guess(), (5, 4, 3, 2))

    def test_last_guess_from_empty_board(self):
        with self.assertRaises(GameBoard.EmptyBoardError):
            self.board.last_guess()

    def test_last_feedback(self):
        self.board.add_guess((1, 2, 3, 4), (2, 1, 0, 1))
        self.board.add_guess((5, 4, 3, 2), (1, 2, 1, 0))
        self.assertEqual(self.board.last_feedback(), (1, 2, 1, 0))

    def test_last_feedback_from_empty_board(self):
        with self.assertRaises(GameBoard.EmptyBoardError):
            self.board.last_feedback()

    def test_remove_last(self):
        self.board.add_guess((1, 2, 3, 4), (2, 1, 0, 1))
        self.board.add_guess((5, 4, 3, 2), (1, 2, 1, 0))
        guess, feedback = self.board.remove_last()
        self.assertEqual(guess, (5, 4, 3, 2))
        self.assertEqual(feedback, (1, 2, 1, 0))
        self.assertEqual(len(self.board), 1)

    def test_remove_last_from_empty_board(self):
        with self.assertRaises(GameBoard.EmptyBoardError):
            self.board.remove_last()

    def test_add_guess(self):
        self.board.add_guess((1, 2, 3, 4), (2, 1, 0, 1))
        self.assertEqual(len(self.board), 1)
        self.assertEqual(self.board.last_guess(), (1, 2, 3, 4))
        self.assertEqual(self.board.last_feedback(), (2, 1, 0, 1))

    def test_clear(self):
        self.board.add_guess((1, 2, 3, 4), (2, 1, 0, 1))
        self.board.add_guess((5, 4, 3, 2), (1, 2, 1, 0))
        self.assertEqual(len(self.board), 2)
        self.board.clear()
        self.assertEqual(len(self.board), 0)


if __name__ == "__main__":
    unittest.main()
