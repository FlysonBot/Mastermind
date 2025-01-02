from dataclasses import fields

from mastermind.client.languages import global_localization
from mastermind.libs.logs import ClientLogger
from mastermind.libs.menus import DynamicMenu, MenuConfig, MenuOption, back
from mastermind.server.database.models import AllSettings

from .menu_handler import MenuHandler

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
            name: str = setting.name
            value: bool = getattr(settings, name)

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
