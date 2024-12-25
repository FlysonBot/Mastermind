from mastermind.client.display.libs.menus import EnumMenu, MenuOption
from mastermind.client.display.libs.menus.back import back
from mastermind.client.display.libs.menus.menu_config import MenuConfig
from mastermind.client.display.tui.menus.load_games import LoadGames
from mastermind.client.display.tui.menus.menu_handler import MenuHandler
from mastermind.client.display.tui.menus.new_game import NewGame
from mastermind.client.display.tui.menus.settings import Settings


class MainMenu(EnumMenu):
    NEW_GAME = MenuOption("Create New Game", "1", lambda: NewGame.activate())
    SAVED_GAME = MenuOption("Load Saved Game", "2", lambda: LoadGames.activate())
    SETTINGS = MenuOption("Settings", "3", lambda: Settings.activate())
    QUIT = MenuOption("Quit", "q", lambda: back)

    @classmethod
    def config(cls) -> MenuConfig:
        return MenuConfig(
            title="Main Menu",
            menu_adapter=MenuHandler,
            stay_in_menu=True,
        )
