from abc import ABC, abstractmethod
from typing import Any


class UserProfile:
    """An utility class to store and access user profile data."""

    @classmethod
    def create_new_user(cls):
        pass


class UserSettings:
    """An utility class to store and access user settings."""


class UserMenus:
    """A collection of user menus."""

    class Menu(ABC):
        """An user menu template. Menu being stored as dictionary."""

        def __new__(cls):
            raise NotImplementedError("Cannot instantiate menu.")

        def __call__(self, length):
            assert len(self) == length, "Menu length mismatch."
            return self.get_option()

        def __len__(self):
            return len(self.menu)

        @classmethod
        def display(cls) -> None:
            """Display the menu."""
            header = f"--- {cls.__name__} ---"

            print("\n\n\n" + header)  # print 3 empty lines and the header
            for key, value in cls.menu.items():  # print the options
                print(f"({key}) {value}")
            print("-"*len(header) + "\n")  # print the separator

        @classmethod
        def get_option(cls) -> str:
            """Get the user's option."""

            cls.display()
            while True:
                option = input("Select an option: ")
                if option in cls.menu:
                    # Return the key can avoid potential mismatch when editing menu
                    return cls.menu[option]
                else:
                    cls.display()
                    print("Invalid option. Try again.")


    class MainMenu(Menu):
        """The main menu."""
        menu = {
            "1": "Start New Game",
            "2": "Load Saved Game",
            "3": "My Statistics",
            "4": "Settings",
            "0": "Save and Exit"
        }
    

    class NewGameMenu(Menu):
        """The menu for starting a new game."""
        menu = {
            "1": "You vs Someone Else",
            "2": "You vs AI",
            "3": "AI vs You",
            "4": "Solve External Game",
            "0": "Return to Main Menu"
        }


class GameStatistics:
    """An utility class to compute and display game statistics."""

class GameSimulator:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CrawlerSingleton, cls).__new__(cls)
        return cls.instance

    def main_menu(self):
        """Display the main menu and handle user input."""
        choice = UserMenus.MainMenu()(5)

        if choice == "Start New Game":
            self.start_new_game()
        elif choice == "Load Saved Game":
            self.load_saved_game()
        elif choice == "My Statistics":
            self.show_statistics()
        elif choice == "Settings":
            self.settings()
        elif choice == "Save and Exit":
            self.save_and_exit()

    def new_game(self):
        """Display the new game menu and handle user input."""
        choice = UserMenus.NewGameMenu()(5)

        if choice == "You vs Someone Else":
            pass
        elif choice == "You vs AI":
            pass
        elif choice == "AI vs You":
            pass
        elif choice == "Solve External Game":
            pass
        elif choice == "Return to Main Menu":
            self.main_menu()

    def run(self):
        pass


if __name__ == "__main__":
    GameSimulator().run()
