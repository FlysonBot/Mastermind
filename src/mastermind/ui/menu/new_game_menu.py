from mastermind.ui.menu.option_menu import OptionMenu


class NewGameMenu(OptionMenu):
    """
    The menu for starting a new game.
    """

    name = "New Game Menu"
    menu = {
        "1": "You vs Someone Else",
        "2": "You vs AI",
        "3": "AI vs You",
        "4": "Solve External Game",
        "0": "Return to Main Menu",
    }
