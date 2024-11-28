from abc import ABC
from typing import Any

from mastermind.validation.base.base import StateValidator


class ValidatedClass(ABC):
    """
    An abstract base class that provides automatic validation of class attributes.

    When accessing or modifying an attribute of a ValidatedClass instance, if the attribute is a StateValidator, its value will be automatically validated and returned or updated.
    """

    def __getattribute__(self, name: str) -> Any:
        """
        Overrides the __getattribute__ method to automatically handle StateValidator attributes.

        Args:
            name (str): The name of the attribute to be accessed.

        Returns:
            Any: The value of the attribute, with any StateValidator instances unwrapped.
        """
        value = super().__getattribute__(name)

        while isinstance(value, StateValidator):
            value = value.value

        return value

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Overrides the __setattr__ method to automatically handle StateValidator attributes.

        Args:
            name (str): The name of the attribute to be set.
            value (Any): The new value to be assigned to the attribute.
        """
        if hasattr(self, name):
            attr = super().__getattribute__(name)

            if isinstance(attr, StateValidator):
                attr.value = value  # invoke setter method to validate modification
                return

        super().__setattr__(name, value)
