from mastermind.ui.menu.option_menu import OptionMenu


class MainMenu(OptionMenu):
    """
    The main menu of the application.
    """

    name = "Main Menu"
    menu = {
        "1": "Start New Game",
        "2": "Load Saved Game",
        "3": "Game History",
        "0": "Save and Exit",
    }
