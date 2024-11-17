from abc import ABC, abstractmethod
from typing import Any

from main.storage_handler import UserData
from main.validation import MaximumAttempts, NumberOfColors, NumberOfDots, ValidatedData
from main.gameboard import Game


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
        def display(cls) -> None:
            """Display the menu."""
            header = f"--- {cls.__name__} ---"

            print("\n\n\n" + header)  # print 3 empty lines and the header
            for key, value in cls.menu.items():  # print the options
                print(f"({key}) {value}")
            print("-" * len(header) + "\n")  # print the separator

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

        menu = {
            "1": "Start New Game",
            "2": "Load Saved Game",
            "3": "My Statistics",
            "4": "Settings",
            "0": "Save and Exit",
        }

    class NewGameMenu(Menu):
        """The menu for starting a new game."""

        menu = {
            "1": "You vs Someone Else",
            "2": "You vs AI",
            "3": "AI vs You",
            "4": "Solve External Game",
            "0": "Return to Main Menu",
        }


class GameStatistics:
    """An utility class to compute and display game statistics."""


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
        cls.save_game(game)  # save the game
    
    @classmethod
    def save_game(cls, game: Game) -> None:
        """Save the game to a file."""
        if "saved_game" not in UserData():  # if the list is empty
            UserData().saved_game = []  # initialize the list
        UserData().save_game += game  # add the game to the list


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

        elif choice == "My Statistics":
            raise NotImplementedError("Statistics not implemented yet.")
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
