from abc import abstractmethod
from typing import Any, Optional

from src.ui.menu.base_menu import BaseMenu


class DataDisplayMenu(BaseMenu):
    def _print_content(self) -> None:
        data = self._fetch_data()
        if data is not None:
            self._render_data(data)
        else:
            print(self._empty_message())

    @abstractmethod
    def _fetch_data(self) -> Optional[Any]:
        pass

    @abstractmethod
    def _render_data(self, data: Any) -> None:
        pass

    @property
    @abstractmethod
    def _empty_message(self) -> str:
        pass
