from typing import Any, Protocol

from .menu_config import MenuConfig
from .menu_option import MenuOptions


class MenuProtocol(Protocol):
    config: MenuConfig
    options: MenuOptions

    def get_selections(self) -> Any: ...

    def activate(self) -> Any: ...
