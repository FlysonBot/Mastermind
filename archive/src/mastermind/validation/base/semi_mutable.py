from typing import Any

from mastermind.validation.base.base import StateValidator
from mastermind.validation.base.exceptions import (
    InvalidModificationError,
    TypeValidationError,
)


class TrueFuse(StateValidator[bool]):
    """
    A StateValidator that can only be initialized to True or False, and can only be modified to True.
    """

    def validate_value(self, value: Any) -> bool:
        """
        Validates the initial value, ensuring it is a boolean.

        Args:
            value (Any): The initial value.

        Returns:
            bool: The validated value.

        Raises:
            TypeValidationError: If the value is not a boolean.
        """
        if not isinstance(value, bool):
            raise TypeValidationError(
                "TrueFuse can only be initialized to True or False"
            )
        return value

    def validate_modifications(self, new_value: Any) -> True:
        """
        Validates the modification to the value, ensuring it is set to True.

        Args:
            new_value (Any): The new value to be set.

        Raises:
            InvalidModificationError: If the new value is not True.
        """
        if new_value is not True:
            raise InvalidModificationError("TrueFuse can only be modified to True")
        return True
