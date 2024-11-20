from abc import abstractmethod
from typing import Any, Optional
from src.ui.menu.base_menu import BaseMenu


class DataDisplayMenu(BaseMenu):
    """Base class for menus that display data."""
    
    def _print_content(self) -> None:
        data = self._fetch_data()
        if data is not None:
            self._render_data(data)
        else:
            print(self._empty_message())
    
    @abstractmethod
    def _fetch_data(self) -> Optional[Any]:
        """Data retrieval strategy - must be implemented by subclasses."""
        pass
        
    @abstractmethod
    def _render_data(self, data: Any) -> None:
        """Data rendering strategy - must be implemented by subclasses."""
        pass
    
    @property
    @abstractmethod
    def _empty_message(self) -> str:
        """Empty state message - must be implemented by subclasses."""
        pass
