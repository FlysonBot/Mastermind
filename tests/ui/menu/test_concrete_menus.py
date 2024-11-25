import unittest
from unittest.mock import MagicMock, call, patch

import pandas as pd

from src.ui.menu.concrete_menus import (
    GameHistoryMenu,
    MainMenu,
    NewGameMenu,
)


class TestMainMenu(unittest.TestCase):
    @patch("builtins.input", return_value="1")
    @patch.object(MainMenu, "_process_option")
    def test_get_option_valid_input(self, mock_process_option, mock_input):
        menu = MainMenu()
        mock_process_option.return_value = "processed_option"
        self.assertEqual(menu.get_option(), "processed_option")
        mock_input.assert_called_once_with("Select an option: ")
        mock_process_option.assert_called_once_with("1")

    def test_process_option(self):
        menu = MainMenu()
        self.assertEqual(menu._process_option("1"), "Start New Game")
        self.assertEqual(menu._process_option("2"), "Load Saved Game")
        self.assertEqual(menu._process_option("3"), "Game History")
        self.assertEqual(menu._process_option("4"), "Settings")
        self.assertEqual(menu._process_option("0"), "Save and Exit")


class TestNewGameMenu(unittest.TestCase):
    def setUp(self):
        self.menu = NewGameMenu()

    def test_name(self):
        self.assertEqual(self.menu.name, "New Game Menu")

    @patch("builtins.input", return_value="2")
    @patch.object(NewGameMenu, "_process_option")
    def test_get_option_valid_input(self, mock_process_option, mock_input):
        mock_process_option.return_value = "processed_option"
        self.assertEqual(self.menu.get_option(), "processed_option")
        mock_input.assert_called_once_with("Select an option: ")
        mock_process_option.assert_called_once_with("2")

    @patch("builtins.input", side_effect=["invalid", "0"])
    @patch.object(NewGameMenu, "display")
    def test_get_option_invalid_input(self, mock_display, mock_input):
        self.assertEqual(self.menu.get_option(), "Return to Main Menu")
        mock_input.assert_has_calls(
            [call("Select an option: "), call("Select an option: ")]
        )
        self.assertEqual(mock_display.call_count, 2)

    def test_process_option(self):
        self.assertEqual(self.menu._process_option("1"), "You vs Someone Else")
        self.assertEqual(self.menu._process_option("2"), "You vs AI")
        self.assertEqual(self.menu._process_option("3"), "AI vs You")
        self.assertEqual(self.menu._process_option("4"), "Solve External Game")
        self.assertEqual(self.menu._process_option("0"), "Return to Main Menu")


class TestGameHistoryMenu(unittest.TestCase):
    def setUp(self):
        self.menu = GameHistoryMenu()

    @patch("src.main.main.GameHistoryManager.retrieve_game_history")
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

    @patch("src.main.main.GameHistoryManager.retrieve_game_history")
    @patch("builtins.print")
    def test_print_content_without_data(self, mock_print, mock_retrieve_game_history):
        mock_retrieve_game_history.return_value = None
        self.menu._print_content()
        mock_retrieve_game_history.assert_called()
        mock_print.assert_called_with("No game history found.")

    def test_fetch_data(self):
        with patch(
            "src.main.main.GameHistoryManager.retrieve_game_history"
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


""" AI Generated Test, couldn't use because main package code had not finish refactor
class TestResumeGameMenu(unittest.TestCase):
    def setUp(self):
        self.menu = ResumeGameMenu()

    @patch.object(GameController, "list_continuable_games")
    @patch.object(GameController, "retrieve_continuable_games")
    @patch("src.utils.render_dataframe")
    def test_init_and_fetch_data(
        self,
        mock_render_dataframe,
        mock_retrieve_continuable_games,
        mock_list_continuable_games,
    ):
        mock_list_continuable_games.return_value = ["Game 1", "Game 2"]
        mock_retrieve_continuable_games.return_value = pd.DataFrame(
            {"Game": ["Game 1", "Game 2"]}
        )

        self.assertDictEqual(
            self.menu.menu, {"0": "Return to Main Menu", "1": "", "2": ""}
        )
        self.assertEqual(
            self.menu._fetch_data().to_dict(),
            pd.DataFrame({"Game": ["Game 1", "Game 2"]}).to_dict(),
        )

    @patch.object(GameController, "list_continuable_games")
    @patch.object(GameController, "retrieve_continuable_games")
    @patch("src.utils.render_dataframe")
    def test_render_data(
        self,
        mock_render_dataframe,
        mock_retrieve_continuable_games,
        mock_list_continuable_games,
    ):
        mock_list_continuable_games.return_value = ["Game 1", "Game 2"]
        mock_retrieve_continuable_games.return_value = pd.DataFrame(
            {"Game": ["Game 1", "Game 2"]}
        )

        with patch("builtins.print") as mock_print:
            self.menu._render_data(self.menu._fetch_data())
            mock_render_dataframe.assert_called_with(
                pd.DataFrame({"Game": ["Game 1", "Game 2"]})
            )
            mock_print.assert_called_with("\n(0) Return to Main Menu")

    def test_get_empty_message(self):
        self.assertEqual(self.menu._get_empty_message(), "No continuable game found.")

    def test_process_option(self):
        self.assertEqual(self.menu._process_option("0"), "return")
        self.assertEqual(self.menu._process_option("1"), 0)
        self.assertEqual(self.menu._process_option("2"), 1)
 """

if __name__ == "__main__":
    unittest.main()
