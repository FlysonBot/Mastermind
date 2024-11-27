from src.main.game_controller import GameController
from src.main.game_storage import list_continuable_games_index, retrieve_stored_games
from src.storage import UserDataManager
from src.ui.menu.concrete_menus import (
    GameHistoryMenu,
    MainMenu,
    NewGameMenu,
    ResumeGameMenu,
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
        choice = MainMenu().get_option()

        if choice == "Start New Game":
            self.new_game_menu()
            return True

        elif choice == "Load Saved Game":
            self.saved_game_menu()
            return True

        elif choice == "Game History":
            GameHistoryMenu().display()
            return True

        elif choice == "Save and Exit":
            return False  # terminate the loop

    def new_game_menu(self) -> bool:
        """Display the new game menu and handle user input."""
        choice = NewGameMenu().get_option()

        if choice == "You vs Someone Else":
            GameController.start_new_game("HvH")
            return True
        elif choice == "You vs AI":
            GameController.start_new_game("HvAI")
            return True
        elif choice == "AI vs You":
            #GameController.start_new_game("AIvH")
            print("This feature  is not implemented yet.")
            return True
        elif choice == "Solve External Game":
            #GameController.start_new_game("AIvAI")
            print("This feature  is not implemented yet.")
            return True
        elif choice == "Return to Main Menu":
            return False  # terminate the loop
        else:
            raise AssertionError("Unexpected invalid choice.")

    def saved_game_menu(self):
        """Display the saved game menu and handle user input."""
        choice = ResumeGameMenu().get_option()

        if choice == 0:
            return False  # return to main menu

        game_index = list_continuable_games_index(retrieve_stored_games())
        GameController.resume_game(game_index[choice-1])  # -1 since first option is 1

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
