from typing import Any, Callable


class CallableString(str):
    """String that can be called as a function.

    Example:
        >>> def plus_one(value: str) -> int:
        ...     return int(value) + 1
        >>> callable_string = CallableString("1", func=plus_one)
        >>> callable_string
        '1'
        >>> callable_string()
        2
        >>> special_str = lambda string: CallableString(string, func=plus_one)
        >>> special_str("1")
        '1'
        >>> special_str("1")()
        2

    """

    def __new__(cls, value: str, func: Callable[[Any], Any]) -> "CallableString":
        return str.__new__(cls, value)

    def __init__(self, value: str, func: Callable[[Any], Any]) -> None:
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(self, *args, **kwargs)
