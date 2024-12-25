from abc import ABC, abstractmethod
from typing import Any

from mastermind.client.display.libs.menus.display_mode import DisplayMode
from mastermind.client.display.libs.menus.menu_option import MenuOptions


class MenuAdapter(ABC):
    """This class is responsible for displaying and handling menu selections."""

    def __init__(
        self,
        title: str,
        menu_options: MenuOptions,
        display_mode: DisplayMode,
        **kwargs: dict[Any, Any],
    ) -> None:
        self.title = title
        self.menu_options = menu_options
        self.display_mode = display_mode
        self.kwargs = kwargs

    @abstractmethod
    def get_selections(self) -> MenuOptions:
        """Display and handle menu selections."""
