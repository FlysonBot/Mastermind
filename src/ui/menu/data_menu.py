from abc import abstractmethod
from typing import Any, Optional

from src.ui.menu.base_menu import BaseMenu


class DataDisplayMenu(BaseMenu):
    """
    An abstract base class for menus that display data.

    Provides common functionality for fetching, rendering, and displaying data.
    """

    def _print_content(self) -> None:
        """
        Prints the content of the menu, which is the data fetched and rendered.
        """
        data = self._fetch_data()
        if data is not None:
            self._render_data(data)
        else:
            print(self._empty_message())

    @abstractmethod
    def _fetch_data(self) -> Optional[Any]:
        """
        Fetches the data to be displayed in the menu.

        This is an abstract method that must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def _render_data(self, data: Any) -> None:
        """
        Renders the data to be displayed in the menu.

        This is an abstract method that must be implemented by subclasses.
        """
        pass

    @property
    @abstractmethod
    def _empty_message(self) -> str:
        """
        Returns the message to be displayed when there is no data to show.

        This is an abstract property that must be implemented by subclasses.
        """
        pass
