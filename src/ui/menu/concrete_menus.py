from typing import Optional, Union

import pandas as pd

from src.main.main import GameHandler, GameHistory
from src.ui.menu.data_menu import DataDisplayMenu
from src.ui.menu.option_menu import OptionMenu
from src.utils import render_dataframe


class MainMenu(OptionMenu):
    name = "Main Menu"
    menu = {
        "1": "Start New Game",
        "2": "Load Saved Game",
        "3": "Game History",
        "4": "Settings",
        "0": "Save and Exit",
    }


class NewGameMenu(OptionMenu):
    name = "New Game Menu"
    menu = {
        "1": "You vs Someone Else",
        "2": "You vs AI",
        "3": "AI vs You",
        "4": "Solve External Game",
        "0": "Return to Main Menu",
    }


class GameHistoryMenu(DataDisplayMenu):
    name = "Game History"
    width = 25

    def _fetch_data(self) -> Optional[pd.DataFrame]:
        return GameHistory.retrieve_game_history()

    def _render_data(self, data: pd.DataFrame) -> None:
        render_dataframe(data)

    def _get_empty_message(self) -> str:
        return "No game history found."

    def display(self) -> None:
        super().display()
        input("\nPress Enter to continue...")


class ResumeGameMenu(DataDisplayMenu):
    name = "Resume Game"
    width = 27

    def __init__(self):
        self.menu = {
            str(index + 1): ""
            for index in range(len(GameHandler.list_continuable_games()))
        }
        self.menu["0"] = "Return to Main Menu"

    def _fetch_data(self) -> Optional[pd.DataFrame]:
        return GameHandler.retrieve_continuable_games()

    def _render_data(self, data: pd.DataFrame) -> None:
        data.index = [f"({i+1})" for i in data.index]
        render_dataframe(data)
        print("\n(0) Return to Main Menu")

    def _get_empty_message(self) -> str:
        return "No continuable game found."

    def _process_option(self, option: str) -> Union[str, int]:
        return "return" if int(option) == 0 else int(option) - 1
