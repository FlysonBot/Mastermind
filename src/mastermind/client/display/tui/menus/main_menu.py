from mastermind.client.display.languages import global_localization
from mastermind.client.display.tui.menus.load_games import LoadGames
from mastermind.client.display.tui.menus.menu_handler import MenuHandler
from mastermind.client.display.tui.menus.new_game import NewGame
from mastermind.client.display.tui.menus.settings import Settings
from mastermind.libs.logs import ClientLogger
from mastermind.libs.menus import EnumMenu, MenuOption
from mastermind.libs.menus.back import back
from mastermind.libs.menus.menu_config import MenuConfig

main_menu = global_localization.menu.main_menu


class MainMenu(EnumMenu):
    NEW_GAME = MenuOption(main_menu.new_game, "1", lambda: NewGame.activate())
    SAVED_GAME = MenuOption(main_menu.saved_game, "2", lambda: LoadGames.activate())
    SETTINGS = MenuOption(main_menu.settings, "3", lambda: Settings.activate())
    QUIT = MenuOption(main_menu.quit, "q", lambda: back)

    @classmethod
    def config(cls) -> MenuConfig:
        return MenuConfig(
            title=main_menu.menu_title,
            menu_adapter=MenuHandler,
            stay_in_menu=True,
            logger=ClientLogger("MainMenu").logger,
        )
