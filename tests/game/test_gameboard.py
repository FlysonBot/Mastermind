import unittest

from unittest.mock import MagicMock
from src.game import Game
from src.players import (
    HumanCracker,
    HumanSetter,
    AISetter,
)


class TestGameboard(unittest.TestCase):

    # Setup method to create a fresh Game instance before each test
    def setUp(self):
        self.game = Game(
            number_of_colors=6, number_of_dots=4, maximum_attempts=10, game_mode="HvH"
        )
        self.board = self.game._board

    # Tests for the _Board class
    def test_board_initialization(self):
        """Test the initialization of the board."""
        self.assertEqual(self.board.NUMBER_OF_COLORS, 6)
        self.assertEqual(self.board.NUMBER_OF_DOTS, 4)
        self.assertEqual(len(self.board), 0)

    def test_board_add_guess(self):
        """Test adding a guess to the board."""
        guess = (1, 2, 3, 4)
        feedback = (2, 1)
        self.board.add_guess(guess, feedback)
        self.assertEqual(len(self.board), 1)
        self.assertEqual(self.board.last_guess(), guess)
        self.assertEqual(self.board.last_feedback(), feedback)

    def test_board_remove_last(self):
        """Test removing the last guess and feedback."""
        guess = (1, 2, 3, 4)
        feedback = (2, 1)
        self.board.add_guess(guess, feedback)
        removed_guess, removed_feedback = self.board.remove_last()
        self.assertEqual(removed_guess, guess)
        self.assertEqual(removed_feedback, feedback)
        self.assertEqual(len(self.board), 0)

    def test_board_empty_error_on_last_guess(self):
        """Test EmptyBoardError when accessing last guess on empty board."""
        with self.assertRaises(Game._Board.EmptyBoardError):
            self.board.last_guess()

    # Tests for the Game class
    def test_game_initialization(self):
        """Test initialization values of Game."""
        self.assertEqual(self.game.MAXIMUM_ATTEMPTS, 10)
        self.assertEqual(self.game.GAME_MODE, "HvH")
        self.assertIsNone(self.game.win_status)
        self.assertFalse(self.game.game_started)

    def test_submit_guess(self):
        """Test submitting a guess."""
        self.board.add_guess = MagicMock()
        self.game.find_players()
        guess = (1, 2, 3, 4)
        feedback = (2, 1)
        self.game.submit_guess(guess, feedback)
        self.board.add_guess.assert_called_once_with(guess, feedback)

    def test_update_win_status_win(self):
        """Test win condition when last guess matches secret code."""
        self.game.SECRET_CODE = (1, 2, 3, 4)
        self.board.add_guess(self.game.SECRET_CODE, (4, 0))
        self.assertTrue(self.game.update_win_status())
        self.assertTrue(self.game.win_status)

    def test_update_win_status_loss(self):
        """Test loss condition when maximum attempts are reached without matching code."""
        for _ in range(self.game.MAXIMUM_ATTEMPTS):
            self.board.add_guess((1, 2, 3, 5), (0, 2))
        self.assertFalse(self.game.update_win_status())
        self.assertFalse(self.game.win_status)

    def test_find_players_HvH(self):
        """Test player initialization for Human vs Human game mode."""
        self.game.find_players()
        self.assertIsInstance(self.game.PLAYER_CRACKER, HumanCracker)
        self.assertIsInstance(self.game.PLAYER_SETTER, HumanSetter)

    def test_find_players_HvAI(self):
        """Test player initialization for Human vs AI game mode."""
        del self.game.GAME_MODE
        self.game.GAME_MODE = "HvAI"
        self.game.find_players()
        self.assertIsInstance(self.game.PLAYER_CRACKER, HumanCracker)
        self.assertIsInstance(self.game.PLAYER_SETTER, AISetter)

    def test_player_guessing_logic_quit(self):
        """Test player_guessing_logic with quit command."""
        self.game.PLAYER_CRACKER = MagicMock()
        self.game.PLAYER_SETTER = MagicMock()
        self.game.PLAYER_CRACKER.obtain_guess.return_value = "q"
        self.assertEqual(self.game.player_guessing_logic(), "q")

    def test_player_guessing_logic_discard(self):
        """Test player_guessing_logic with quit command."""
        self.game.PLAYER_CRACKER = MagicMock()
        self.game.PLAYER_SETTER = MagicMock()
        self.game.PLAYER_CRACKER.obtain_guess.return_value = "d"
        self.assertEqual(self.game.player_guessing_logic(), "d")

    def test_output_result_win(self):
        """Test output result when game is won."""
        self.game.PLAYER_CRACKER = MagicMock()
        self.game._win_status = True
        self.game.update_win_status = lambda: None
        self.game.output_result()
        self.game.PLAYER_CRACKER.win_message.assert_called_once()

    def test_output_result_loss(self):
        """Test output result when game is lost."""
        self.game.PLAYER_CRACKER = MagicMock()
        self.game._win_status = False
        self.game.update_win_status = lambda: None
        self.game.output_result()
        self.game.PLAYER_CRACKER.lose_message.assert_called_once()

    def test_start_game_already_started(self):
        """Test start_game raises error if game already started."""
        self.game._game_started = True
        with self.assertRaises(NotImplementedError):
            self.game.start_game()

    def test_start_game_initialization(self):
        """Test start_game initializes the game properly."""
        self.game.find_players = MagicMock()
        self.game.PLAYER_SETTER = MagicMock()
        self.game.player_guessing_logic = MagicMock(return_value=None)
        self.game.start_game()
        self.assertTrue(self.game._game_started)
        self.game.find_players.assert_called_once()
        self.game.PLAYER_SETTER.set_secret_code.assert_called_once()


# Run the test suite
if __name__ == "__main__":
    unittest.main()
