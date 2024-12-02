from typing import Optional

import pandas as pd

from mastermind.main.game_history import GameHistoryManager
from mastermind.ui.menu.data_menu import DataDisplayMenu
from mastermind.utils.render_dataframe import render_dataframe


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
