from typing import Any, Callable


class CallableString(str):
    """String class that can be called like a function"""

    def __new__(cls, value: str, func: Callable[[Any], Any]) -> "CallableString":
        return str.__new__(cls, value)

    def __init__(self, value: str, func: Callable[[Any], Any]) -> None:
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(self, *args, **kwargs)
