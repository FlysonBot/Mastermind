from dataclasses import field
from typing import Any, NamedTuple, Type

from mastermind.client.display.libs.menus.display_mode import DisplayMode
from mastermind.client.display.libs.menus.menu_adapter import MenuAdapter


class MenuConfig(NamedTuple):
    title: str
    menu_adapter: Type[MenuAdapter]
    display_mode: DisplayMode = DisplayMode.BOTH
    stay_in_menu: bool = False
    kwargs: dict[Any, Any] = field(default_factory=dict)
