from abc import abstractmethod
from typing import Optional

from mastermind.client.display.libs.menus.back import back
from mastermind.client.display.libs.menus.menu_config import MenuConfig
from mastermind.client.display.libs.menus.menu_option import MenuOptions
from mastermind.libs.utils import EnumMeta


class EnumMenu(EnumMeta):
    @classmethod
    @abstractmethod
    def config(cls) -> MenuConfig:
        pass

    @classmethod
    def list_options(cls) -> MenuOptions:
        # member is a MenuOption
        return [member.value for member in cls]

    @classmethod
    def get_selections(cls) -> MenuOptions:
        config = cls.config()
        selection = config.menu_adapter(
            config.title, cls.list_options(), config.display_mode
        ).get_selections()

        cls.config().logger.debug(f"Selections: {selection}")

        return selection

    @classmethod
    def activate(cls, stay_in_menu: Optional[bool] = False) -> None:
        stay_in_menu = stay_in_menu or cls.config().stay_in_menu

        cls.config().logger.debug(
            f"Activating menu: {cls.__name__}. Stay in menu: {stay_in_menu}"
        )

        while (
            cls.get_selections()[0].action() is not back and cls.config().stay_in_menu
        ):
            pass
