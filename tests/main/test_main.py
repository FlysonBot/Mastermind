import unittest
from unittest.mock import MagicMock, call, create_autospec, patch

from mastermind.main.main import MainUI
from mastermind.storage.user_data import UserDataManager


class TestMainUI(unittest.TestCase):
    """Unit tests for the MainUI class"""

    @patch("mastermind.ui.menu.MainMenu.get_option", return_value="Start New Game")
    @patch("mastermind.main.main.MainUI.new_game_menu", return_value=True)
    def test_main_menu_start_new_game(self, mock_new_game_menu, mock_get_option):
        """Test the main menu when user chooses to start a new game"""
        main_ui = MainUI()
        self.assertTrue(main_ui.main_menu())
        mock_get_option.assert_called_once()
        mock_new_game_menu.assert_called_once()

    @patch("mastermind.ui.menu.MainMenu.get_option", return_value="Load Saved Game")
    @patch("mastermind.main.main.MainUI.saved_game_menu", return_value=True)
    def test_main_menu_load_saved_game(self, mock_saved_game_menu, mock_get_option):
        """Test the main menu when user chooses to load a saved game"""
        main_ui = MainUI()
        self.assertTrue(main_ui.main_menu())
        mock_get_option.assert_called_once()
        mock_saved_game_menu.assert_called_once()

    @patch("mastermind.ui.menu.MainMenu.get_option", return_value="Game History")
    @patch("mastermind.ui.menu.GameHistoryMenu.display")
    def test_main_menu_game_history(self, mock_display, mock_get_option):
        """Test the main menu when user chooses to view game history"""
        main_ui = MainUI()
        self.assertTrue(main_ui.main_menu())
        mock_get_option.assert_called_once()
        mock_display.assert_called_once()

    @patch("mastermind.ui.menu.MainMenu.get_option", return_value="Save and Exit")
    def test_main_menu_save_and_exit(self, mock_get_option):
        """Test the main menu when user chooses to save and exit"""
        main_ui = MainUI()
        self.assertFalse(main_ui.main_menu())
        mock_get_option.assert_called_once()

    @patch(
        "mastermind.ui.menu.NewGameMenu.get_option", return_value="You vs Someone Else"
    )
    @patch("mastermind.main.game_controller.GameController.start_new_game")
    def test_new_game_menu_human_vs_human(self, mock_start_new_game, mock_get_option):
        """Test the new game menu when user chooses to play against another human"""
        main_ui = MainUI()
        self.assertTrue(main_ui.new_game_menu())
        mock_get_option.assert_called_once()
        mock_start_new_game.assert_called_once_with("HvH")

    @patch("mastermind.ui.menu.NewGameMenu.get_option", return_value="You vs AI")
    @patch("mastermind.main.game_controller.GameController.start_new_game")
    def test_new_game_menu_human_vs_ai(self, mock_start_new_game, mock_get_option):
        """Test the new game menu when user chooses to play against the AI"""
        main_ui = MainUI()
        self.assertTrue(main_ui.new_game_menu())
        mock_get_option.assert_called_once()
        mock_start_new_game.assert_called_once_with("HvAI")

    @patch("mastermind.ui.menu.NewGameMenu.get_option", return_value="AI vs You")
    @patch("builtins.print")
    def test_new_game_menu_ai_vs_human(self, mock_print, mock_get_option):
        """Test the new game menu when user chooses the AI vs Human mode (not implemented)"""
        main_ui = MainUI()
        self.assertTrue(main_ui.new_game_menu())
        mock_get_option.assert_called_once()
        mock_print.assert_called_once_with("This feature  is not implemented yet.")

    @patch(
        "mastermind.ui.menu.NewGameMenu.get_option", return_value="Return to Main Menu"
    )
    def test_new_game_menu_return_to_main(self, mock_get_option):
        """Test the new game menu when user chooses to return to the main menu"""
        main_ui = MainUI()
        self.assertFalse(main_ui.new_game_menu())
        mock_get_option.assert_called_once()

    @patch("mastermind.ui.menu.NewGameMenu.get_option", return_value="Invalid Choice")
    def test_new_game_menu_invalid_choice(self, mock_get_option):
        """Test the new game menu when user makes an invalid choice"""
        main_ui = MainUI()
        with self.assertRaises(AssertionError):
            main_ui.new_game_menu()
        mock_get_option.assert_called_once()

    @patch("mastermind.ui.menu.ResumeGameMenu.get_option", return_value=0)
    def test_saved_game_menu_return_to_main(self, mock_get_option):
        """Test the saved game menu when user chooses to return to the main menu"""
        main_ui = MainUI()
        self.assertFalse(main_ui.saved_game_menu())
        mock_get_option.assert_called_once()

    @patch(
        "mastermind.main.main.list_continuable_games_index",
        return_value=[0],
    )
    @patch("mastermind.main.game_controller.GameController.resume_game")
    @patch("mastermind.ui.menu.ResumeGameMenu.get_option", return_value=1)
    def test_saved_game_menu_resume_game(
        self, mock_get_option, mock_resume_game, mock_list_continuable_games_index
    ):
        """Test the saved game menu when user chooses to resume a game"""
        main_ui = MainUI()
        self.assertTrue(main_ui.saved_game_menu())
        mock_get_option.assert_called_once()
        mock_list_continuable_games_index.assert_called_once()
        mock_resume_game.assert_called_once_with(0)  # index 0 for option 1

    @patch("builtins.print")
    def test_run_main_loop(self, mock_print):
        """Test the main loop of the MainUI"""
        mock_user_data_manager = create_autospec(UserDataManager, instance=True)
        mock_user_data_manager.save_data = MagicMock()

        with patch("mastermind.main.main.userdata", new=mock_user_data_manager):
            with patch(
                "mastermind.main.main.MainUI.main_menu", side_effect=[True, True, False]
            ):
                main_ui = MainUI()
                main_ui.run()

            mock_print.assert_has_calls(
                [call("Welcome to Mastermind!"), call("Thank you for playing!")]
            )
            mock_user_data_manager.save_data.assert_called_once()


if __name__ == "__main__":
    unittest.main()
