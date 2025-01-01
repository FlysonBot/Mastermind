from mastermind.client.display.languages import global_localization
from mastermind.client.display.libs.menus.back import back
from mastermind.client.display.libs.menus.enum_menu import EnumMenu
from mastermind.client.display.libs.menus.menu_config import MenuConfig
from mastermind.client.display.libs.menus.menu_option import MenuOption
from mastermind.client.display.tui.menus.menu_handler import MenuHandler
from mastermind.libs.logs import ClientLogger
from mastermind.server.database.enum.game_mode import GameMode

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
