from abc import ABC, abstractmethod
from typing import Any

from mastermind.libs.menus.display_mode import DisplayMode
from mastermind.libs.menus.menu_option import MenuOptions


class MenuAdapter(ABC):
    """This class is responsible for displaying and handling menu selections.

    This adapter ensure the underlying ui handling is separated from the menu logic, allowing for flexible ui implementations and consistent interface.
    """

    def __init__(
        self,
        title: str,
        menu_options: MenuOptions,
        display_mode: DisplayMode,
        **kwargs: dict[Any, Any],
    ) -> None:
        self.title: str = title
        self.menu_options = menu_options
        self.display_mode: DisplayMode = display_mode
        self.kwargs: dict[str, dict[Any, Any]] = kwargs

    @abstractmethod
    def get_selections(self) -> MenuOptions:
        """Display and handle menu selections."""
