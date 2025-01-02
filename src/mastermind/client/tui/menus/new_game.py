from mastermind.client.languages import global_localization
from mastermind.libs.logs import ClientLogger
from mastermind.libs.menus import EnumMenu, MenuConfig, MenuOption, back
from mastermind.server.database.enum import GameMode

from .menu_handler import MenuHandler

new_game = global_localization.menu.new_game_menu


class NewGame(EnumMenu):
    PVP = MenuOption(new_game.PVP, "1", lambda: create_new_game(GameMode.PVP))
    PVC = MenuOption(new_game.PVC, "2", lambda: create_new_game(GameMode.PVC))
    CVP = MenuOption(new_game.CVP, "3", lambda: create_new_game(GameMode.CVP))
    EVE = MenuOption(new_game.EVE, "4", lambda: create_new_game(GameMode.EVE))
    BACK = MenuOption(
        global_localization.menu.menu_handler.return_to_main, "r", lambda: back
    )

    @classmethod
    def config(cls) -> MenuConfig:
        return MenuConfig(
            title=new_game.menu_title,
            menu_adapter=MenuHandler,
            stay_in_menu=False,
            logger=ClientLogger("NewGame").logger,
        )


def create_new_game(game_mode: GameMode) -> None: ...
