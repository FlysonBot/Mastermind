import pandas as pd

from mastermind.database.models.game import Game
from mastermind.display.libs.menus.back import back
from mastermind.display.libs.menus.dynamic_menu import DynamicMenu
from mastermind.display.libs.menus.menu_config import MenuConfig
from mastermind.display.libs.menus.menu_option import MenuOption
from mastermind.display.tui.menus.menu_handler import MenuHandler
from mastermind.libs.utils import render_dataframe


def example_load_api() -> list[Game]: ...
def example_play_api(index: int) -> None: ...


class LoadGames(DynamicMenu):
    config = MenuConfig(
        title="Load Games",
        menu_adapter=MenuHandler,
        stay_in_menu=False,
    )

    @classmethod
    def reconstruct_menu(cls) -> None:
        cls.options = []

        table = pd.DataFrame(example_load_api())
        rendered = render_dataframe(table)

        for i, line in enumerate(rendered):
            cls.add_option(MenuOption(line, str(i), lambda: example_play_api(i)))

        cls.add_option(MenuOption("Return to Main Menu", "r", lambda: back))
