from typing import Any, Protocol

from mastermind.display.libs.menus.menu_config import MenuConfig
from mastermind.display.libs.menus.menu_option import MenuOptions


class MenuProtocol(Protocol):
    config: MenuConfig
    options: MenuOptions

    def get_selections(self) -> Any: ...

    def activate(self) -> Any: ...
