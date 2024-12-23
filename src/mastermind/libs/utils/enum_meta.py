from enum import Enum


class EnumMeta(Enum):
    """Metaclass for enums that contain a customized __repr__ method.

    This metaclass has a customized __repr__ method that return the name of the enum member directly instead of the memory address.

    Example:
        >>> class MyEnum(EnumMeta):
        ...     A = "A"
        >>> MyEnum.A
        MyEnum.A
        >>> repr(MyEnum.A)
        'MyEnum.A'
        >>> class DefaultEnum(Enum):
        ...     A = "A"
        >>> DefaultEnum.A
        <DefaultEnum.A: 'A'>
    """

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
