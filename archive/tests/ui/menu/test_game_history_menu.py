import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from mastermind.ui.menu.game_history_menu import GameHistoryMenu


class TestGameHistoryMenu(unittest.TestCase):
    def setUp(self):
        self.menu = GameHistoryMenu()

    @patch("mastermind.main.game_history.GameHistoryManager.retrieve_game_history")
    def test_print_content_with_data(self, mock_retrieve_game_history):
        mock_retrieve_game_history.return_value = pd.DataFrame(
            {"Game": ["Game 1", "Game 2"]}
        )
        self.menu._render_data = MagicMock()
        with patch("builtins.print") as mock_print:
            self.menu._print_content()
            mock_retrieve_game_history.assert_called()
            self.menu._render_data.assert_called_with(
                mock_retrieve_game_history.return_value
            )
            mock_print.assert_not_called()

    @patch("mastermind.main.game_history.GameHistoryManager.retrieve_game_history")
    @patch("builtins.print")
    def test_print_content_without_data(self, mock_print, mock_retrieve_game_history):
        mock_retrieve_game_history.return_value = None
        self.menu._print_content()
        mock_retrieve_game_history.assert_called()
        mock_print.assert_called_with("No game history found.")

    def test_fetch_data(self):
        with patch(
            "mastermind.main.game_history.GameHistoryManager.retrieve_game_history"
        ) as mock_retrieve_game_history:
            mock_retrieve_game_history.return_value = pd.DataFrame(
                {"Game": ["Game 1", "Game 2"]}
            )
            self.assertEqual(
                self.menu._fetch_data().to_dict(),
                pd.DataFrame({"Game": ["Game 1", "Game 2"]}).to_dict(),
            )

    @patch("builtins.input", return_value="")
    def test_display(self, mock_input):
        with patch.object(GameHistoryMenu, "_print_content") as mock_print_content:
            self.menu.display()
            mock_print_content.assert_called()
            mock_input.assert_called_once_with("\nPress Enter to continue...")
