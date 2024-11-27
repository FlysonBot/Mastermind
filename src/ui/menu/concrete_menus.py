from typing import Optional, Union

import pandas as pd

from src.main.game_controller import GameController
from src.main.game_history import GameHistoryManager
from src.ui.menu.data_menu import DataDisplayMenu
from src.ui.menu.option_menu import OptionMenu
from src.utils import render_dataframe


class MainMenu(OptionMenu):
    """
    The main menu of the application.
    """

    name = "Main Menu"
    menu = {
        "1": "Start New Game",
        "2": "Load Saved Game",
        "3": "Game History",
        "4": "Settings",
        "0": "Save and Exit",
    }


class NewGameMenu(OptionMenu):
    """
    The menu for starting a new game.
    """

    name = "New Game Menu"
    menu = {
        "1": "You vs Someone Else",
        "2": "You vs AI",
        "3": "AI vs You",
        "4": "Solve External Game",
        "0": "Return to Main Menu",
    }


class GameHistoryMenu(DataDisplayMenu):
    """
    The menu for displaying the game history.
    """

    name = "Game History"
    width = 25

    def _fetch_data(self) -> Optional[pd.DataFrame]:
        """
        Retrieves the game history data.
        """
        return GameHistoryManager.retrieve_game_history()

    def _render_data(self, data: pd.DataFrame) -> None:
        """
        Renders the game history data.
        """
        render_dataframe(data)

    def _empty_message(self) -> str:
        """
        Returns the message to display when there is no game history.
        """
        return "No game history found."

    def display(self) -> None:
        """
        Displays the game history menu and waits for user input to continue.
        """
        super().display()
        input("\nPress Enter to continue...")


class ResumeGameMenu(DataDisplayMenu):
    """
    The menu for resuming a saved game.
    """

    name = "Resume Game"
    width = 27

    def __init__(self):
        """
        Initializes the menu with the list of continuable games.
        """
        games = GameController.list_continuable_games()
        self.menu = {"0": "Return to Main Menu"}
        for i in range(len(games)):
            self.menu[str(i + 1)] = ""

    def _fetch_data(self) -> Optional[pd.DataFrame]:
        """
        Retrieves the list of continuable games.
        """
        return GameController.retrieve_continuable_games()

    def _render_data(self, data: pd.DataFrame) -> None:
        """
        Renders the list of continuable games.
        """
        data.index = [f"({i+1})" for i in data.index]
        render_dataframe(data)
        print("\n(0) Return to Main Menu")

    def _empty_message(self) -> str:
        """
        Returns the message to display when there are no continuable games.
        """
        return "No continuable game found."

    def _process_option(self, option: str) -> Union[str, int]:
        """
        Processes the selected option, returning either "return" or the index of the selected game.
        """
        return "return" if int(option) == 0 else int(option) - 1
