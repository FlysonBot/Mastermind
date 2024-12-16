from typing import Any, Dict, TypeVar, Union

VT = TypeVar("VT")  # Type for value in a key-value pair


class DotDict(Dict[str, Any]):
    """Dictionary that supports dot notation for accessing nested keys.
    
    Example:
        >>> normal_dict = {"a": {"b": 1, "c": {"d": 2}}}
        >>> dot_dict = DotDict(normal_dict)
        >>> dot_dict.a.b
        1
        >>> dot_dict.a.c.d
        2
        >>> dot_dict["a"]["b"]
        1
        >>> dot_dict["a"]["c"]["d"]
        2
        >>> dot_dict.a
        {'b': 1, 'c': {'d': 2}}
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self.update(*args, **kwargs)

    def update(self, *args: Dict[str, VT], **kwargs: VT) -> None:  # type: ignore
        """Update the DotDict object with the provided arguments."""

        def convert(value: VT) -> Union[DotDict, VT]:
            return DotDict(value) if isinstance(value, dict) else value

        for arg in args:
            for key, value in arg.items():
                self[key] = convert(value)

        for key, value in kwargs.items():
            self[key] = convert(value)

    def __getattr__(self, key: str) -> Any:
        return self.__getitem__(key)

    def __setattr__(self, key: str, value: Any) -> None:
        self.__setitem__(key, value)

    def __delattr__(self, item: str) -> None:
        return self.__delitem__(item)
