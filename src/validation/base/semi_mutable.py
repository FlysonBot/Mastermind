from typing import Any

from src.validation.base.base import StateValidator
from src.validation.base.exceptions import (
    InvalidModificationError,
    TypeValidationError,
)


class TrueFuse(StateValidator[bool]):
    def validate_value(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise TypeValidationError(
                "TrueFuse can only be initialized to True or False"
            )
        return value

    def validate_modifications(self, new_value: Any) -> None:
        if new_value is not True:
            raise InvalidModificationError("TrueFuse can only be modified to True")
