from src.main.game_controller import GameController
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
            # return True

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
