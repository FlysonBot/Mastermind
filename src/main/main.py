from typing import Any, List, Optional

import pandas as pd

from src.game import Game
from src.storage import UserDataManager
from src.ui.menu.concrete_menus import (
    GameHistoryMenu,
    MainMenu,
    NewGameMenu,
    ResumeGameMenu,
)
from src.validation import (
    MaximumAttempts,
    NumberOfColors,
    NumberOfDots,
    Validator,
)


class GameHistoryManager:
    """Store and retrieve game history."""

    @classmethod
    def generate_meta_data(cls, game: Game) -> dict:
        """Generate meta data for the game."""
        return {
            "game_mode": game.GAME_MODE,
            "number_of_dots": game.number_of_dots,
            "number_of_colors": game.number_of_colors,
            "amount_attempted": len(game),
            "amount_allowed": game.MAXIMUM_ATTEMPTS,
            "win_status": game.win_status,
            "guesses": game._board._guesses,
            "feedback": game._board._feedbacks,
            **({"game": game} if game.win_status is None else {}),
        }

    @classmethod
    def save_game(cls, game: Game) -> None:
        """Save the game to a file."""
        if "saved_games" not in UserDataManager():  # if the list is empty
            UserDataManager().saved_games = []  # initialize the list

        UserDataManager().saved_games.append(
            cls.generate_meta_data(game)
        )  # store the meta data

    @classmethod
    def retrieve_game_history(cls) -> Optional[pd.DataFrame]:
        return GameController.game_listing(UserDataManager().saved_games)


class GameController:
    """Communication between MainUI and the gameboard."""

    @classmethod
    def validate_input(cls, prompt: str, validator: Validator) -> Any:
        """Get user input and validate it."""
        while True:
            try:
                user_input = input("\n" + prompt)
                if validator(user_input):
                    return user_input
                else:
                    print("Invalid input. Please try again.")

            except Exception as e:
                print(f"Invalid input. {e}")

    @classmethod
    def get_game_parameters(cls) -> tuple[int, int, int]:
        """Get the number of colors, number of dots, and number of rounds from user."""
        num_of_colors = cls.validate_input(
            "Enter the number of colors (2-10): ", NumberOfColors
        )
        num_of_dots = cls.validate_input(
            "Enter the number of dots (2-10): ", NumberOfDots
        )
        max_attempts = cls.validate_input(
            "Enter the maximum number of attempts: ", MaximumAttempts
        )
        return num_of_colors, num_of_dots, max_attempts

    @classmethod
    def start_new_game(cls, game_mode: str) -> None:
        """Start a new game."""
        if game_mode not in ["HvH", "HvAI", "AIvH", "AIvAI"]:
            raise AssertionError("Unexpected invalid game mode.")

        parameters = cls.get_game_parameters()  # get user input
        game = Game(*parameters, game_mode)  # create a new game
        game.start_game()  # start the game
        GameHistoryManager.save_game(game)  # save the game

    @classmethod
    def list_continuable_games(cls, return_index: bool = False) -> List[dict]:
        """Get the saved game from the user."""
        saved_games = UserDataManager().saved_games

        if not return_index:
            return [game for game in saved_games if game["win_status"] is None]

        else:
            return [
                index
                for index, game in enumerate(saved_games)
                if game["win_status"] is None
            ]

    @classmethod
    def retrieve_continuable_games(cls) -> Optional[pd.DataFrame]:
        """List the saved game from the user as pandas table."""
        return cls.game_listing(cls.list_continuable_games())

    @classmethod
    def game_listing(cls, games: List[dict]) -> Optional[pd.DataFrame]:
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

    @classmethod
    def resume_game(cls, game_index: int) -> None:
        """Resume a saved game."""
        # Retrieve game
        saved_games = UserDataManager().saved_games
        game = UserDataManager().saved_games[game_index]["game"]

        # Resume game
        game.resume_game()

        # Update saved games
        UserDataManager().saved_games[game_index] = (
            GameHistoryManager().generate_meta_data(game)
        )


class MainUI:
    """Class to handle the user menu interface."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MainUI, cls).__new__(cls)
        return cls.instance

    def main_menu(self) -> bool:
        """
        Display the main menu and handle user input.
        Return whether the user want to exit.
        """
        choice = MainMenu()

        if choice == "Start New Game":
            self.new_game_menu()
            return True

        elif choice == "Load Saved Game":
            self.saved_game_menu()
            return True

        elif choice == "Game History":
            GameHistoryMenu.display()
            input("\nPress Enter to continue...")
            return True

        elif choice == "Settings":
            raise NotImplementedError("Settings not implemented yet.")
            return True

        elif choice == "Save and Exit":
            return False  # terminate the loop

    def new_game_menu(self) -> bool:
        """Display the new game menu and handle user input."""
        choice = NewGameMenu()

        if choice == "You vs Someone Else":
            GameController.start_new_game("HvH")
            return True
        elif choice == "You vs AI":
            GameController.start_new_game("HvAI")
            return True
        elif choice == "AI vs You":
            GameController.start_new_game("AIvH")
            return True
        elif choice == "Solve External Game":
            GameController.start_new_game("AIvAI")
            return True
        elif choice == "Return to Main Menu":
            return False  # terminate the loop
        else:
            raise AssertionError("Unexpected invalid choice.")

    def saved_game_menu(self):
        """Display the saved game menu and handle user input."""
        choice = ResumeGameMenu()(len(GameController.list_continuable_games()) + 1)

        if choice == "return":
            return False  # return to main menu

        game_index = GameController.list_continuable_games(return_index=True)[choice]
        GameController.resume_game(game_index)

        return True

    def run(self):
        """Run the game."""
        print("Welcome to Mastermind!")
        while self.main_menu():
            pass  # keep calling self.main_menu() until it return False
        print("Thank you for playing!")
        UserDataManager().save_data()


if __name__ == "__main__":
    MainUI().run()
