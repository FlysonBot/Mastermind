import unittest
from unittest.mock import MagicMock, patch

from mastermind.game.game import Game
from mastermind.game.game_flow import GameFlow


class TestGameFlow(unittest.TestCase):
    def setUp(self):
        self.game = Game(6, 4, 10, "HvH")
        self.game_state = self.game._state
        self.game_flow = self.game._game_flow

    @patch("mastermind.players.HumanCodeSetter.set_secret_code", return_value=(1, 2, 3, 4))
    def test_start_game_not_started(self, mock_set_secret_code):
        self.game_flow._play_game = MagicMock(return_value=None)
        self.assertIsNone(self.game_flow.start_game())
        mock_set_secret_code.assert_called()
        self.assertTrue(self.game_state.game_started)

    def test_start_game_already_started(self):
        self.game_state.game_started = True
        with self.assertRaises(NotImplementedError):
            self.game_flow.start_game()

    def test_resume_game_not_started(self):
        with self.assertRaises(NotImplementedError):
            self.game_flow.resume_game()

    def test_resume_game_started(self):
        self.game_state.game_started = True
        with patch.object(self.game_flow, "_play_game") as mock_play_game:
            self.game_flow.resume_game()
            mock_play_game.assert_called()

    @patch("mastermind.game.player_logic.PlayerLogic.process_player_guessing")
    @patch.object(GameFlow, "output_result")
    def test_play_game(self, mock_output_result, mock_process_player_guessing):
        mock_process_player_guessing.return_value = "q"
        self.assertEqual(self.game_flow._play_game(), "q")
        mock_process_player_guessing.assert_called()
        mock_output_result.assert_called()

    def test_output_win(self):  # sourcery skip: extract-duplicate-method
        self.game._player_logic.initialize_players()

        self.game._player_logic.PLAYER_CRACKER.win_message = MagicMock()
        self.game_state.check_and_update_win_status = MagicMock(return_value=True)
        self.game_state._win_status = True
        self.game_flow.output_result()
        self.game._player_logic.PLAYER_CRACKER.win_message.assert_called()

    def test_output_lose(self):
        self.game._player_logic.initialize_players()

        self.game._player_logic.PLAYER_CRACKER.lose_message = MagicMock()
        self.game_state.check_and_update_win_status = MagicMock(return_value=False)
        self.game_state._win_status = False
        self.game_flow.output_result()
        self.game._player_logic.PLAYER_CRACKER.lose_message.assert_called()

    def test_output_continue(self):
        self.game._player_logic.initialize_players()

        self.game_state.check_and_update_win_status = MagicMock(return_value=None)
        self.game_state._win_status = None
        self.assertIsNone(self.game_flow.output_result())


if __name__ == "__main__":
    unittest.main()
