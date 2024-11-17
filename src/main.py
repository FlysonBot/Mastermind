from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from main.gameboard import Game
from main.storage_handler import UserData
from main.validation import MaximumAttempts, NumberOfColors, NumberOfDots, ValidatedData


class UserSettings:
    """An utility class to store and access user settings."""


class UserMenus:
    """A collection of user menus."""

    class Menu(ABC):
        """
        An abstract base class for creating interactive menus.

        This class provides a structure for displaying a menu,
        and getting user options. It serves as a foundation for
        specific menu implementations by defining common behaviors
        for displaying options and handling user input.
        """

        def __call__(self, length):
            """Display the menu and get the user's option when called."""
            assert len(self) == length, "Menu length mismatch."
            return self.get_option()

        def __len__(self):
            """Return the number of options in the menu."""
            return len(self.menu)

        @classmethod
        def get_name(cls) -> str:
            return cls.name if hasattr(cls, "name") else cls.__name__

        @classmethod
        def print_header(cls) -> None:
            """Print the header of the menu."""
            header: str = f"--- {cls.get_name()} ---"
            print("\n\n\n" + header)  # print 3 empty lines and the header

        @classmethod
        def print_options(cls) -> None:
            """Print the options of the menu."""
            for key, value in cls.menu.items():  # print the options
                print(f"({key}) {value}")

        @classmethod
        def print_separator(cls) -> None:
            """Print the separator of the menu."""
            header: str = f"--- {cls.get_name()} ---"
            print("-" * len(header) + "\n")  # print the separator

        @classmethod
        def display(cls) -> None:
            """Display the menu."""
            cls.print_header()
            cls.print_options()
            cls.print_separator()

        @classmethod
        def get_option(cls) -> str:
            """Get the user's option."""

            cls.display()
            while True:
                option = input("Select an option: ")
                if option in cls.menu:
                    # Return the key can avoid potential mismatch when editing menu
                    return cls.menu[option]
                cls.display()
                print("Invalid option. Try again.")

    class MainMenu(Menu):
        """The main menu."""

        name = "Main Menu"
        menu = {
            "1": "Start New Game",
            "2": "Load Saved Game",
            "3": "Game History",
            "4": "Settings",
            "0": "Save and Exit",
        }

    class NewGameMenu(Menu):
        """The menu for starting a new game."""

        name = "New Game Menu"
        menu = {
            "1": "You vs Someone Else",
            "2": "You vs AI",
            "3": "AI vs You",
            "4": "Solve External Game",
            "0": "Return to Main Menu",
        }

    class GameHistoryMenu(Menu):
        """The menu for displaying game history"""

        name = "Game History"

        @classmethod
        def display(cls) -> None:
            """Display the menu."""
            cls.print_header()

            if game_history := GameHistory.retrieve_game_history():
                print(game_history)
            else:
                print("No game history found.")

            cls.print_separator()


class GameHistory:
    """Store and retrieve game history."""

    @classmethod
    def get_meta_data(cls, game: Game) -> dict:
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
        }

    @classmethod
    def save_game(cls, game: Game) -> None:
        """Save the game to a file."""
        if "saved_games" not in UserData():  # if the list is empty
            UserData().saved_games = []  # initialize the list

        UserData().saved_games += cls.get_meta_data(game)  # store the meta data

    @classmethod
    def retrieve_game_history(cls) -> pd.DataFrame:
        if not UserData().saved_games:  # checking
            return None

        dataframe = pd.DataFrame(UserData().saved_games)  # convert to dataframe
        history = pd.DataFrame()  # holder for new dataframe

        # Building the history table
        history["Mode"] = dataframe["game_mode"]
        history["Dimension"] = (
            dataframe["number_of_dots"] + "x" + dataframe["number_of_dots"]
        )
        dataframe["win_status"].replace({True: "W", False: "L", None: " "})
        history["Attempt"] = (
            dataframe["win_status"]
            + " "
            + dataframe["amount_attempted"].astype(str)
            + "/"
            + dataframe["amount_allowed"].astype(str)
        )

        return history


class GameHandler:
    """Communication between MainUI and the gameboard."""

    @classmethod
    def validate_input(cls, prompt: str, validator: ValidatedData) -> Any:
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
        GameHistory.save_game(game)  # save the game


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
        choice = UserMenus.MainMenu()(5)

        if choice == "Start New Game":
            self.new_game_menu()
            return True

        elif choice == "Load Saved Game":
            self.saved_game_menu()
            return True

        elif choice == "Game History":
            UserMenus.GameHistoryMenu.display()
            input("\nPress Enter to continue...")
            return True

        elif choice == "Settings":
            raise NotImplementedError("Settings not implemented yet.")
            return True

        elif choice == "Save and Exit":
            return False  # terminate the loop

    def new_game_menu(self) -> bool:
        """Display the new game menu and handle user input."""
        choice = UserMenus.NewGameMenu()(5)

        if choice == "You vs Someone Else":
            GameHandler.start_new_game("HvH")
            return True
        elif choice == "You vs AI":
            GameHandler.start_new_game("HvAI")
            return True
        elif choice == "AI vs You":
            GameHandler.start_new_game("AIvH")
            return True
        elif choice == "Solve External Game":
            GameHandler.start_new_game("AIvAI")
            return True
        elif choice == "Return to Main Menu":
            return False  # terminate the loop
        else:
            raise AssertionError("Unexpected invalid choice.")

    def saved_game_menu(self):
        """Display the saved game menu and handle user input."""
        pass

    def run(self):
        """Run the game."""
        print("Welcome to Mastermind!")
        while self.main_menu():
            pass  # keep calling self.main_menu() until it return False
        print("Thank you for playing!")
        UserData().save_data()


if __name__ == "__main__":
    MainUI().run()
