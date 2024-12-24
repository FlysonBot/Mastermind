from abc import abstractmethod
from typing import NamedTuple, Type

from mastermind.display.libs.menus.display_mode import DisplayMode
from mastermind.display.libs.menus.menu_adapter import MenuAdapter
from mastermind.display.libs.menus.menu_option import MenuOptions
from mastermind.libs.utils import EnumMeta

EnumMenuConfig = NamedTuple(
    "EnumMenuConfig",
    [
        ("title", str),
        ("display_mode", DisplayMode),
        ("menu_adapter", Type[MenuAdapter]),
    ],
)


class EnumMenu(EnumMeta):
    @classmethod
    @abstractmethod
    def config(cls) -> EnumMenuConfig:
        pass

    @classmethod
    def list_options(cls) -> MenuOptions:
        # member is a MenuOption
        return [member.value for member in cls]

    @classmethod
    def get_selections(cls) -> MenuOptions:
        config = cls.config()
        return config.menu_adapter(
            config.title, cls.list_options(), config.display_mode
        ).get_selections()
