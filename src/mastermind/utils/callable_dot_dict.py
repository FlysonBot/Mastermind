from typing import Any, Callable

from mastermind.utils.callable_string import CallableString
from mastermind.utils.dot_dict import DotDict


class CallableDotDict(DotDict):
    """DotDict that wraps string values in CallableString"""

    def __init__(self, *args: Any, func: Callable[[Any], Any], **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__func = func

    def __getattr__(self, key: str) -> Any:
        value = super().__getattr__(key)

        if isinstance(value, dict):  # Wrap dictionary to support nested dot notation
            return CallableDotDict(value, func=self.__func)

        if isinstance(value, str):  # Wrap string to support callable dot notation
            return CallableString(value, func=self.__func)

        return value
