from typing import Any, Callable, NamedTuple


class MenuOption(NamedTuple):
    title: str  # the name of the option, i.e. "Quit"
    value: str  # the index of the option, i.e. "1", "a", ...
    action: Callable[[], Any]  # a function to call when option selected


MenuOptions = list[MenuOption]
