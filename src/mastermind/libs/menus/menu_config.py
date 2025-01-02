from dataclasses import field
from logging import Logger
from typing import Any, NamedTuple, Type


from ..logs import NullLogger
from .display_mode import DisplayMode
from .menu_adapter import MenuAdapter


class MenuConfig(NamedTuple):
    title: str
    menu_adapter: Type[MenuAdapter]
    display_mode: DisplayMode = DisplayMode.BOTH
    stay_in_menu: bool = False
    logger: Logger = NullLogger("NullLogger")
    kwargs: dict[Any, Any] = field(default_factory=dict)
