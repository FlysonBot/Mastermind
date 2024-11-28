from typing import List, Optional

import pandas as pd

from mastermind.game.game import Game
from mastermind.main.game_storage import list_continuable_games, retrieve_stored_games
from mastermind.storage.user_data import UserDataManager


def game_list_to_pandas(games: List[dict]) -> Optional[pd.DataFrame]:
    if not games:  # no games
        return None

    dataframe = pd.DataFrame(games)  # convert to dataframe
    listing = pd.DataFrame()  # holder for new dataframe

    # Building the listing
    dataframe["win_status"] = dataframe["win_status"].replace(
        {True: "W", False: "L", None: " "}  # win, lost, continue
    )  # change the win status to human readable format

    listing["Mode"] = dataframe["game_mode"]
    listing["Dimension"] = (
        dataframe["number_of_colors"].astype(str)
        + "x"
        + dataframe["number_of_dots"].astype(str)
    )  # express the colors and dots together as a dimension
    listing["Attempts"] = (
        dataframe["win_status"].astype(str)
        + " "
        + dataframe["amount_attempted"].astype(str)
        + "/"
        + dataframe["amount_allowed"].astype(str)
    )

    return listing


class GameHistoryManager:
    """Store and retrieve game history."""

    @staticmethod
    def generate_meta_data(game: Game) -> dict:
        """Generate meta data for the game."""
        return {
            "game_mode": game._state.GAME_MODE,
            "number_of_dots": game._state.number_of_dots,
            "number_of_colors": game._state.number_of_colors,
            "amount_attempted": len(game),
            "amount_allowed": game._state.MAXIMUM_ATTEMPTS,
            "win_status": game._state.win_status,
            "guesses": game._board._guesses,
            "feedback": game._board._feedbacks,
            **({"game": game} if game._state.win_status is None else {}),
        }

    @staticmethod
    def save_game(game: Game) -> None:
        """Save the game to a file."""
        if "saved_games" not in UserDataManager():  # if the list is empty
            UserDataManager().saved_games = []  # initialize the list

        UserDataManager().saved_games.append(
            GameHistoryManager.generate_meta_data(game)
        )  # store the meta data

    @staticmethod
    def retrieve_game_history() -> Optional[pd.DataFrame]:
        return game_list_to_pandas(retrieve_stored_games())

    @staticmethod
    def retrieve_continuable_games() -> Optional[pd.DataFrame]:
        return game_list_to_pandas(list_continuable_games(retrieve_stored_games()))
