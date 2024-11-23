from abc import abstractmethod
from numbers import Number
from typing import Optional, TypeVar

from src.validation.base.base import ValidationModel
from src.validation.base.exceptions import (
    InputConversionError,
    RangeError,
    TypeValidationError,
)

T = TypeVar("T", bound=Number)


class NumberRangeModel(ValidationModel[T]):
    """
    A ValidationModel that validates numeric values within a specified range.

    Attributes:
        gt (Optional[Number]): The minimum value (exclusive).
        lt (Optional[Number]): The maximum value (exclusive).
        ge (Optional[Number]): The minimum value (inclusive).
        le (Optional[Number]): The maximum value (inclusive).
    """

    def __init__(
        self,
        gt: Optional[Number] = None,
        lt: Optional[Number] = None,
        ge: Optional[Number] = None,
        le: Optional[Number] = None,
    ) -> None:
        """
        Initializes the NumberRangeModel with the specified range constraints.
        """
        super().__init__(gt=gt, lt=lt, ge=ge, le=le)

    def validate_arguments(self) -> None:
        """
        Validates the range constraints provided to the NumberRangeModel.
        """
        if self.gt and self.ge:
            raise ValueError("gt and ge cannot be used together")

        if self.lt and self.le:
            raise ValueError("lt and le cannot be used together")

        min_value = self.gt or self.ge
        max_value = self.lt or self.le

        if min_value and max_value and min_value >= max_value:
            raise ValueError("Range maximum cannot be less than or equal to minimum")

    def validate_value(self, value: Number | str) -> Number:
        """
        Validates the given value and returns the validated value.

        Args:
            value (Number | str): The value to be validated.

        Returns:
            Number: The validated value.

        Raises:
            TypeValidationError: If the value is not a number or a string.
            InputConversionError: If the value cannot be converted to the expected numeric type.
            RangeError: If the value is outside the specified range.
        """
        if isinstance(value, str):
            value = self.convert(value)

        elif not isinstance(value, Number):
            raise TypeValidationError("Invalid type for number validation")

        self.validate_range(value)

        return value

    @abstractmethod
    def convert(self, value: str) -> Number:
        """
        Converts the given string value to the expected numeric type.

        Args:
            value (str): The string value to be converted.

        Returns:
            Number: The converted numeric value.

        Raises:
            InputConversionError: If the value cannot be converted to the expected numeric type.
        """
        pass

    def validate_range(self, value: Number) -> None:
        """
        Validates that the given value is within the specified range.

        Args:
            value (Number): The value to be validated.

        Raises:
            RangeError: If the value is outside the specified range.
        """
        if self.gt and value <= self.gt:
            raise RangeError(f"Value must be greater than {self.gt}")
        if self.ge and value < self.ge:
            raise RangeError(f"Value must be greater than or equal to {self.ge}")
        if self.lt and value >= self.lt:
            raise RangeError(f"Value must be less than {self.lt}")
        if self.le and value > self.le:
            raise RangeError(f"Value must be less than or equal to {self.le}")


class ConstrainedInteger(NumberRangeModel[int]):
    """
    A NumberRangeModel that validates integer values within a specified range.
    """

    def convert(self, value: str) -> int:
        """
        Converts the given string value to an integer.

        Args:
            value (str): The string value to be converted.

        Returns:
            int: The converted integer value.

        Raises:
            InputConversionError: If the value cannot be converted to an integer.
        """
        try:
            return int(value)
        except ValueError as e:
            raise InputConversionError("Invalid input for integer conversion") from e


class ConstrainedFloat(NumberRangeModel[float]):
    """
    A NumberRangeModel that validates float values within a specified range.
    """

    def convert(self, value: str) -> float:
        """
        Converts the given string value to a float.

        Args:
            value (str): The string value to be converted.

        Returns:
            float: The converted float value.

        Raises:
            InputConversionError: If the value cannot be converted to a float.
        """
        try:
            return float(value)
        except ValueError as e:
            raise InputConversionError("Invalid input for float conversion") from e
