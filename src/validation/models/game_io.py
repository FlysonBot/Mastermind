from typing import Any, Tuple

from src.validation.base import (
    InputConversionError,
    TypeValidationError,
    ValidationModel,
)
from src.validation.models.numeric import NumberOfColors, NumberOfDots


class _GameValidationUtils:
    """Utility class for game validation."""

    @staticmethod
    def convert(value: str) -> Tuple[int, ...]:
        """Convert string input to tuple of integers."""
        try:
            if "," in value:  # i.e. "1,2,3"
                return tuple(map(int, value.split(",")))
            return tuple(map(int, value))  # if "123"

        except ValueError as e:
            raise InputConversionError("Invalid combination format") from e

    @staticmethod
    def validate_arguments(instance) -> None:
        NumberOfDots().validate(instance.n_of_dots)
        NumberOfColors().validate(instance.n_of_colors)


class ValidCombination(ValidationModel[Tuple[int, ...]]):
    """Validates a color combination."""

    def __init__(self, number_of_dots: int, number_of_colors: int) -> None:
        self.convert = lambda value: _GameValidationUtils.convert(value)
        self.validate_arguments = lambda: _GameValidationUtils.validate_arguments(self)
        super().__init__(
            n_of_dots=number_of_dots,
            n_of_colors=number_of_colors,
        )

    def validate(self, value: Any) -> Tuple[int, ...]:
        if isinstance(value, str):
            value = self.convert(value)

        if not isinstance(value, (tuple, list)):
            raise TypeValidationError("A combination must be a tuple of integers")

        self.validate_combination(value)

        return tuple(value)

    def validate_combination(self, combination: Tuple[int, ...]) -> None:
        if len(combination) != self.n_of_dots:
            raise ValueError(f"Combination must have {self.n_of_dots} dots")

        for dot in combination:
            if dot < 1 or dot > self.n_of_colors or not isinstance(dot, int):
                raise ValueError(
                    f"Dots must be integers between 1 and {self.n_of_colors}"
                )


class ValidFeedback(ValidationModel[Tuple[int, int]]):
    """Validates game feedback."""

    def __init__(self, number_of_dots: int) -> None:
        super().__init__(number_of_dots=number_of_dots)

    def validate_arguments(self) -> None:
        if not hasattr(self, "number_of_dots"):
            raise ValueError("number_of_dots is required")

    def convert(self, value: str) -> Tuple[int, int]:
        """Convert string input to tuple of two integers."""
        try:
            if "," in value:
                return tuple(map(int, value.split(",")))
            return tuple(map(int, value))
        except ValueError as e:
            raise InputConversionError("Invalid feedback format") from e

    def validate(self, value: Any) -> Tuple[int, int]:
        if isinstance(value, str):
            value = self.convert(value)

        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeValidationError("Feedback must be a tuple of two integers")

        for num in value:
            if not isinstance(num, int) or num < 0 or num > self.number_of_dots:
                raise ValueError(
                    f"Feedback values must be between 0 and {self.number_of_dots}"
                )

        return value
