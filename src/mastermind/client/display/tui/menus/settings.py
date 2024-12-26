from dataclasses import fields

from mastermind.client.display.languages import global_localization
from mastermind.client.display.libs.menus.back import back
from mastermind.client.display.libs.menus.dynamic_menu import DynamicMenu
from mastermind.client.display.libs.menus.menu_config import MenuConfig
from mastermind.client.display.libs.menus.menu_option import MenuOption
from mastermind.client.display.tui.menus.menu_handler import MenuHandler
from mastermind.libs.logs import ClientLogger
from mastermind.server.database.models.settings import AllSettings

settings = AllSettings()
settings_menu = global_localization.menu.settings


class Settings(DynamicMenu):
    config = MenuConfig(
        title=settings_menu.menu_title,
        menu_adapter=MenuHandler,
        stay_in_menu=True,
        logger=ClientLogger("Settings").logger,
        kwargs={"input_hint": settings_menu.input_hint},
    )

    @classmethod
    def reconstruct_menu(cls) -> None:
        cls.options = []

        for i, setting in enumerate(fields(settings)):
            name = setting.name
            value = getattr(settings, name)

            cls.add_option(
                MenuOption(
                    f"{name}: {value}",
                    str(i),
                    lambda: setattr(settings, name, not value),
                )
            )

        cls.add_option(
            MenuOption(
                global_localization.menu.menu_handler.return_to_main, "r", lambda: back
            )
        )
