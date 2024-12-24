from abc import ABC, abstractmethod

from mastermind.display.libs.menus.display_mode import DisplayMode
from mastermind.display.libs.menus.menu_option import MenuOptions


class MenuAdapter(ABC):
    """This class is responsible for displaying and handling menu selections."""

    def __init__(
        self, title: str, menu_options: MenuOptions, display_mode: DisplayMode
    ) -> None:
        self.title = title
        self.menu_options = menu_options
        self.display_mode = display_mode

    @abstractmethod
    def get_selections(self) -> MenuOptions:
        """Display and handle menu selections."""
