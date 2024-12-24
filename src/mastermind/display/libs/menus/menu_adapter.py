from abc import ABC, abstractmethod

from mastermind.display.libs.menus.display_mode import DisplayMode
from mastermind.display.libs.menus.menu_option import MenuOptions


class MenuAdapter(ABC):
    """This class is responsible for displaying and handling menu selections."""

    def __init__(self, menu_options: MenuOptions, display_mode: DisplayMode) -> None:
        self.menu_options = menu_options
        self.display_mode = display_mode

    @abstractmethod
    def show(self) -> MenuOptions:
        """Display and handle menu selections."""