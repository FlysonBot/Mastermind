from abc import abstractmethod
from numbers import Number
from typing import Any, Optional

from src.validation.base.base import ValidationModel
from src.validation.base.exceptions import (
    InputConversionError,
    RangeError,
    TypeValidationError,
)


class NumberRangeModel(ValidationModel[Number]):
    """Validates numbers within a specified range."""

    def __init__(
        self,
        gt: Optional[Number] = None,
        lt: Optional[Number] = None,
        ge: Optional[Number] = None,
        le: Optional[Number] = None,
    ) -> None:
        super().__init__(gt=gt, lt=lt, ge=ge, le=le)

    def validate_arguments(self) -> None:
        """Validate the keyword arguments."""
        if self.gt and self.ge:
            raise ValueError("gt and ge cannot be used together")

        if self.lt and self.le:
            raise ValueError("lt and le cannot be used together")

        if (self.gt or self.ge) <= (self.lt or self.le):
            raise ValueError("Range maximum cannot be less than or equals to minimum")

    def validate(self, value: Number | str) -> Number:
        if isinstance(value, str):
            value = self.convert(value)

        elif not isinstance(value, Number):
            raise TypeValidationError("Invalid type for number validation")

        self.validate_range(value)

        return value

    @abstractmethod
    def convert(self, value: str) -> Number:
        """Convert string input to number."""
        pass

    def validate_range(self, value: Number) -> None:
        """Validate if the number is within the specified range."""

        if self.gt and value <= self.gt:
            raise RangeError(f"Value must be greater than {self.gt}")
        if self.ge and value < self.ge:
            raise RangeError(f"Value must be greater than or equal to {self.ge}")
        if self.lt and value >= self.lt:
            raise RangeError(f"Value must be less than {self.lt}")
        if self.le and value > self.le:
            raise RangeError(f"Value must be less than or equal to {self.le}")


class ConstrainedInteger(NumberRangeModel[int]):
    """Validates integers within a specified range."""

    def convert(self, value: str) -> int:
        """Convert string input to integer."""
        try:
            return int(value)
        except ValueError as e:
            raise InputConversionError("Invalid input for integer conversion") from e


class ConstrainedFloat(NumberRangeModel[float]):
    """Validates floats within a specified range."""

    def convert(self, value: str) -> float:
        """Convert string input to float."""
        try:
            return float(value)
        except ValueError as e:
            raise InputConversionError("Invalid input for float conversion") from e
