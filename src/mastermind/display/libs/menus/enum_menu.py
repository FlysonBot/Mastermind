from abc import abstractmethod
from typing import Type

from mastermind.display.libs.menus.menu_adapter import MenuAdapter
from mastermind.display.libs.menus.menu_option import MenuOptions
from mastermind.libs.utils import EnumMeta


class EnumMenu(EnumMeta):
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def menu_adapter(self) -> Type[MenuAdapter]:
        pass

    @classmethod
    def list_options(cls) -> MenuOptions:
        # member is a MenuOption
        return [member.value for member in cls]

    @classmethod
    def get_selection(cls) -> MenuOptions:
        return cls.menu_adapter(cls.list_options()).show()  # type: ignore
