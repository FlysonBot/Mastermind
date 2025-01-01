import pandas as pd

from mastermind.client.languages import global_localization
from mastermind.client.tui.menus.menu_handler import MenuHandler
from mastermind.libs.logs import ClientLogger
from mastermind.libs.menus import DynamicMenu, MenuConfig, MenuOption, back
from mastermind.libs.utils import render_dataframe
from mastermind.server.database.models import Game


def example_load_api() -> list[Game]: ...
def example_play_api(index: int) -> None: ...


class LoadGames(DynamicMenu):
    config = MenuConfig(
        title=global_localization.menu.load_games.menu_title,
        menu_adapter=MenuHandler,
        stay_in_menu=False,
        logger=ClientLogger("LoadGames").logger,
    )

    @classmethod
    def reconstruct_menu(cls) -> None:
        cls.options = []

        table = pd.DataFrame(example_load_api())
        rendered: list[str] = render_dataframe(table)

        for i, line in enumerate(rendered):
            cls.add_option(MenuOption(line, str(i), lambda: example_play_api(i)))

        cls.add_option(
            MenuOption(
                global_localization.menu.menu_handler.return_to_main, "r", lambda: back
            )
        )
