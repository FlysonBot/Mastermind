import unittest
from unittest.mock import patch

from mastermind.game.game import Game
from mastermind.players import (
    AICodeCracker,
    AICodeSetter,
    ExternalCodeSetter,
    HumanCodeCracker,
    HumanCodeSetter,
)


class TestPlayerLogic(unittest.TestCase):
    def setUp(self):
        self.game = Game(6, 4, 10, "HvH")
        self.player_logic = self.game._player_logic

    def _check_players(self, expected_cracker, expected_setter):
        self.player_logic.initialize_players()
        self.assertIsInstance(self.player_logic.PLAYER_CRACKER, expected_cracker)
        self.assertIsInstance(self.player_logic.PLAYER_SETTER, expected_setter)

    def test_initialize_players_HvH(self):
        self._check_players(HumanCodeCracker, HumanCodeSetter)

    def test_initialize_players_HvAI(self):
        self.player_logic.game_state.GAME_MODE = "HvAI"
        self._check_players(HumanCodeCracker, AICodeSetter)

    def test_initialize_players_AIvH(self):
        self.player_logic.game_state.GAME_MODE = "AIvH"
        self._check_players(AICodeCracker, HumanCodeSetter)

    def test_initialize_players_AIvAI(self):
        self.player_logic.game_state.GAME_MODE = "AIvAI"
        self._check_players(AICodeCracker, ExternalCodeSetter)

    @patch("mastermind.players.HumanCodeCracker.obtain_guess")
    @patch("mastermind.players.AICodeSetter.get_feedback")
    def test_process_player_guessing(self, mock_get_feedback, mock_obtain_guess):
        mock_obtain_guess.side_effect = [(1, 2, 3, 4), "q"]
        mock_get_feedback.side_effect = [(2, 2)]

        self.player_logic.game_state.GAME_MODE = (
            "HvAI"  # for easier testing (mock output)
        )
        self.player_logic.initialize_players()
        self.assertEqual(self.player_logic.process_player_guessing(), "q")
        self.assertEqual(list(self.game._board._guesses), [(1, 2, 3, 4)])
        self.assertEqual(list(self.game._board._feedbacks), [(2, 2)])

    @patch("mastermind.players.HumanCodeCracker.obtain_guess")
    @patch("mastermind.players.AICodeSetter.get_feedback")
    def test_process_player_cracker_undo_and_redo(
        self, mock_get_feedback, mock_obtain_guess
    ):
        mock_obtain_guess.side_effect = [(1, 2, 3, 4), "u", "r", (1, 2, 3, 5), "d"]
        mock_get_feedback.side_effect = [(2, 2), (2, 1)]
        self.player_logic.game_state.GAME_MODE = "HvAI"
        self.player_logic.initialize_players()

        self.assertEqual(self.player_logic.process_player_guessing(), "d")
        self.assertEqual(list(self.game._board._guesses), [(1, 2, 3, 4), (1, 2, 3, 5)])
        self.assertEqual(list(self.game._board._feedbacks), [(2, 2), (2, 1)])

    @patch("mastermind.players.HumanCodeCracker.obtain_guess")
    @patch("mastermind.players.AICodeSetter.get_feedback")
    def test_process_player_setter_undo(self, mock_get_feedback, mock_obtain_guess):
        mock_obtain_guess.side_effect = [(1, 2, 3, 4), (1, 2, 3, 5), (1, 2, 3, 6)]
        mock_get_feedback.side_effect = [(2, 2), "u", "q"]
        self.player_logic.game_state.GAME_MODE = "HvAI"
        self.player_logic.initialize_players()

        self.assertEqual(self.player_logic.process_player_guessing(), "q")
        self.assertEqual(list(self.game._board._guesses), [(1, 2, 3, 4)])
        self.assertEqual(list(self.game._board._feedbacks), [(2, 2)])

    def test_cannot_make_guess_after_game_ended(self):
        self.game._state._win_status = True
        self.player_logic.game_state.GAME_MODE = "HvAI"
        self.player_logic.initialize_players()
        with self.assertRaises(NotImplementedError):
            self.player_logic.submit_guess((1, 2, 3, 4), (1, 2))


if __name__ == "__main__":
    unittest.main()
