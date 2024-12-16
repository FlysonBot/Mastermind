from typing import Any, Callable

from mastermind.utils.callable_string import CallableString
from mastermind.utils.dot_dict import DotDict


class CallableDotDict(DotDict):
    """DotDict that wraps string values in CallableString
    
    Example:
        >>> def plus_one(value: str) -> int:
        ...     return int(value) + 1
        >>> callable_dot_dict = CallableDotDict({"a": "1", "b": "2"}, func=plus_one)
        >>> callable_dot_dict.a
        '1'
        >>> callable_dot_dict.a()
        2
    """

    def __init__(self, *args: Any, func: Callable[[Any], Any], **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        super().__setattr__("func", func)

    def __getattr__(self, key: str) -> Any:
        value = super().__getattr__(key)

        if isinstance(value, dict):  # Wrap dictionary to support nested dot notation
            return CallableDotDict(value, func=self.func)

        if isinstance(value, str):  # Wrap string to support callable dot notation
            return CallableString(value, func=self.func)

        return value
