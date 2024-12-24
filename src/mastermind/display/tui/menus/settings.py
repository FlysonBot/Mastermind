from dataclasses import fields

from mastermind.database.models.settings import AllSettings
from mastermind.display.libs.menus.back import back
from mastermind.display.libs.menus.dynamic_menu import DynamicMenu
from mastermind.display.libs.menus.menu_config import MenuConfig
from mastermind.display.libs.menus.menu_option import MenuOption
from mastermind.display.tui.menus.menu_handler import MenuHandler

settings = AllSettings()


class Settings(DynamicMenu):
    config = MenuConfig(
        title="Settings",
        menu_adapter=MenuHandler,
        stay_in_menu=True,
        kwargs={"input_hint": "Enter the setting to toggle: "},
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

        cls.add_option(MenuOption("Return to Main Menu", "r", lambda: back))
