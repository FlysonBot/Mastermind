from enum import Enum
from typing import Type, TypeVar

from mastermind.server.database import converter


T = TypeVar("T", bound=Enum)


def serialize_enum_name_only(enum_cls: Type[T]) -> Type[T]:
    """Decorator for enum classes to unstructure and structure by name only.

    Work by registering a custom converter hook to the cattrs converter.

    Args:
        enum_cls (Type[T]): The enum class to register.

    Returns:
        Type[T]: The decorated enum class.

    Example:
        >>> from enum import Enum
        >>> from mastermind.server.database import converter
        >>> @serialize_enum_name_only
        ... class MyEnum(Enum):
        ...     A = "A"
        ...     B = "B"
        >>> converter.unstructure(MyEnum.A)
        'A'
        >>> converter.structure("A", MyEnum)
        <MyEnum.A: 'A'>
    """

    converter.register_structure_hook(enum_cls, lambda d, _: enum_cls[d])
    converter.register_unstructure_hook(enum_cls, lambda d: d.name)

    return enum_cls
