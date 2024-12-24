from abc import ABC

from mastermind.display.libs.menus.menu_adapter import MenuAdapter
from mastermind.display.libs.menus.menu_option import MenuOption, MenuOptions


class DynamicMenu(ABC):
    menu_adapter: MenuAdapter

    def __init__(self, title: str) -> None:
        self.title = title
        self.options: MenuOptions = []

    def add_option(self, option: MenuOption) -> None:
        self.options.append(option)

    def get_selections(self) -> MenuOptions:  # in case of multiple selections
        return self.menu_adapter.get_selections()

