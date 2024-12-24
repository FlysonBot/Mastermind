from mastermind.database.enum.game_mode import GameMode
from mastermind.display.libs.menus.back import back
from mastermind.display.libs.menus.enum_menu import EnumMenu
from mastermind.display.libs.menus.menu_config import MenuConfig
from mastermind.display.libs.menus.menu_option import MenuOption
from mastermind.display.tui.menus.menu_handler import MenuHandler


class NewGame(EnumMenu):
    PVP = MenuOption("You Set You Guess", "1", lambda: create_new_game(GameMode.PVP))
    PVC = MenuOption("You Set Others Guess", "2", lambda: create_new_game(GameMode.PVC))
    CVP = MenuOption("Others Set You Guess", "3", lambda: create_new_game(GameMode.CPV))
    EVE = MenuOption("Solve External Game", "4", lambda: create_new_game(GameMode.EVE))
    BACK = MenuOption("Return to Main Menu", "r", lambda: back)

    @classmethod
    def config(cls) -> MenuConfig:
        return MenuConfig(
            title="New Game",
            menu_adapter=MenuHandler,
            stay_in_menu=False,
        )


def create_new_game(game_mode: GameMode) -> None: ...
