from enum import Enum
from typing import Type, TypeVar

from dataclasses_json import global_config

T = TypeVar("T", bound=Enum)


def serialize_enum_name_only(enum_cls: Type[T]) -> Type[T]:
    """Decorator to register an enum class for name-only JSON serialization with dataclasses-json library.

    Args:
        enum_cls (Type[T]): The enum class to register.

    Returns:
        Type[T]: The decorated enum class.

    Example:
        >>> from dataclasses_json import dataclass_json
        >>> from mastermind.utils.enum_meta import EnumMeta
        >>> from dataclasses import dataclass

        >>> class CustomClass:
        ...     def __repr__(self) -> str:
        ...         return "CustomClass()"

        >>> @serialize_enum_name_only
        ... class MyEnum(EnumMeta):
        ...     A = CustomClass

        >>> @dataclass_json
        ... @dataclass
        ... class MyDataClass:
        ...     my_enum: MyEnum

        >>> my_data_class = MyDataClass(my_enum=MyEnum.A)
        >>> print(my_data_class.to_json())
        {"my_enum": "A"}
        >>> print(MyDataClass.from_json('{"my_enum": "A"}'))
        MyDataClass(my_enum=MyEnum.A)

        >>> class DefaultEnum(Enum):
        ...     A = CustomClass
        >>> @dataclass_json
        ... @dataclass
        ... class DefaultDataClass:
        ...     default_enum: DefaultEnum

        >>> default_data_class = DefaultDataClass(default_enum=DefaultEnum.A)
        >>> print(default_data_class.to_json())
        Traceback (most recent call last):
        ...
        TypeError: Object of type type is not JSON serializable

    """

    def enum_name_encoder(enum_value: Enum) -> str:
        return enum_value.name

    def enum_name_decoder(value: str) -> Enum:
        return enum_cls[value]

    global_config.encoders[enum_cls] = enum_name_encoder  # type: ignore
    global_config.decoders[enum_cls] = enum_name_decoder  # type: ignore

    return enum_cls
