from typing import Any

from src.validation.base.base import StateValidator
from src.validation.base.exceptions import (
    InvalidModificationError,
    TypeValidationError,
)


class TrueFuse(StateValidator[bool]):
    """A boolean that can only be set to True once. Can be initialized to False."""

    def validate(self, value: Any) -> bool:
        """Validate the initial value and set the fuse."""
        if not isinstance(value, bool):
            raise TypeValidationError(
                "TrueFuse can only be initialized to True or False"
            )
        return value

    def validate_modifications(self, new_value: Any) -> None:
        """Validate modifications to the value."""
        if new_value is not True:
            raise InvalidModificationError("TrueFuse can only be modified to True")
