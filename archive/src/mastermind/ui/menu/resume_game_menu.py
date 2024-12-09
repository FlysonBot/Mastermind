from typing import Optional, Union

import pandas as pd

from mastermind.main.game_history import GameHistoryManager
from mastermind.ui.menu.data_menu import DataDisplayMenu
from mastermind.utils.render_dataframe import render_dataframe


class ResumeGameMenu(DataDisplayMenu):
    """
    The menu for resuming a saved game.
    """

    name = "Resume Game"
    width = 27
    _empty_message = "No continuable game found."

    def __init__(self):
        """
        Initializes the menu with the list of continuable games.
        """
        self.menu = {"0": "Return to Main Menu"}

    def _fetch_data(self) -> Optional[pd.DataFrame]:
        """
        Retrieves the list of continuable games.
        """
        result = GameHistoryManager().retrieve_continuable_games()
        self.menu_length = len(result) if result is not None else 0
        return result

    def _render_data(self, data: pd.DataFrame) -> None:
        """
        Renders the list of continuable games.
        """
        data.index = [f"({i+1})" for i in data.index]
        render_dataframe(data)
        print("\n(0) Return to Main Menu")

    def _process_option(self, option: str) -> Union[str, int]:
        """
        Processes the selected option, returning either "return" or the index of the selected game.
        """
        return "return" if int(option) == 0 else int(option) - 1

    def get_option(self) -> Union[str, int]:
        """
        Displays the menu and returns the selected option.
        """
        self.display()
        if self.menu_length == 0:
            input("\nPress Enter to continue...")
            return 0

        while True:
            option = input("Select a game to resume: ")

            if _is_option_valid(option, self.menu_length):
                return int(option)

            print("Invalid input or option. Try again.")
            self.display()


def _is_option_valid(option: str, number_of_options: int) -> bool:
    return option.isdigit() and 0 <= int(option) <= number_of_options
