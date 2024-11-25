from typing import Any, Tuple

from src.validation.base import (
    InputConversionError,
    RangeError,
    TypeValidationError,
    ValidationModel,
)
from src.validation.models.numeric import NumberOfColors, NumberOfDots


class _GameValidationUtils:
    """
    Utility class for validating game-related inputs.
    """

    @staticmethod
    def convert(value: str) -> Tuple[int, ...]:
        """
        Converts a string representation of a combination or feedback into a tuple of integers.

        Args:
            value (str): The string value to be converted.

        Returns:
            Tuple[int, ...]: The converted tuple of integers.

        Raises:
            InputConversionError: If the input string cannot be converted to a valid tuple of integers.
        """
        try:
            if "," in value:  # i.e. "1,2,3"
                return tuple(map(int, value.split(",")))
            return tuple(map(int, value))  # if "123"

        except ValueError as e:
            raise InputConversionError("Invalid combination format") from e

    @staticmethod
    def validate_arguments(instance) -> None:
        """
        Validates the arguments used to initialize the game-related validation models.

        Args:
            instance: The instance of the game-related validation model.
        """
        NumberOfDots().validate_value(instance.n_of_dots)
        NumberOfColors().validate_value(instance.n_of_colors)

    @staticmethod
    def validate_integer_range(values: int, low_limit: int, high_limit: int) -> None:
        for value in values:
            if not isinstance(value, int):
                raise TypeValidationError(
                    f"Value {value} is not an integer"
                )
            
            if value < low_limit or value > high_limit:
                raise RangeError(
                    f"Value {value} is not in range [{low_limit}, {high_limit}]"
                )


class ValidCombination(ValidationModel[Tuple[int, ...]]):
    """
    A ValidationModel that validates a combination of dots in a game.

    Attributes:
        n_of_dots (int): The number of dots in the combination.
        n_of_colors (int): The number of colors available for the dots.
    """

    def __init__(self, number_of_dots: int, number_of_colors: int) -> None:
        """
        Initializes the ValidCombination with the number of dots and colors.
        """
        self.convert = lambda value: _GameValidationUtils.convert(value)
        self.validate_arguments = lambda: _GameValidationUtils.validate_arguments(self)
        super().__init__(
            n_of_dots=number_of_dots,
            n_of_colors=number_of_colors,
        )

    def validate_value(self, value: Any) -> Tuple[int, ...]:
        """
        Validates the given combination and returns the validated combination.

        Args:
            value (Any): The combination to be validated.

        Returns:
            Tuple[int, ...]: The validated combination.

        Raises:
            TypeValidationError: If the combination is not a tuple or list of integers.
            RangeError: If the combination does not have the correct number of dots or the dot values are not within the valid range.
        """
        if isinstance(value, str):
            value = self.convert(value)

        if not isinstance(value, (tuple, list)):
            raise TypeValidationError(
                "A combination must be a tuple or list of integers"
            )

        if len(value) != self.n_of_dots:
            raise RangeError(f"Combination must have {self.n_of_dots} dots")

        _GameValidationUtils.validate_integer_range(value, 1, self.n_of_colors)

        return tuple(value)


class ValidFeedback(ValidationModel[Tuple[int, int]]):
    """
    A ValidationModel that validates the feedback for a game.

    Attributes:
        number_of_dots (int): The number of dots in the combination.
    """

    def __init__(self, number_of_dots: int) -> None:
        """
        Initializes the ValidFeedback with the number of dots.
        """
        self.convert = lambda value: _GameValidationUtils.convert(value)
        super().__init__(number_of_dots=number_of_dots)

    def validate_arguments(self) -> None:
        """
        Validates the arguments used to initialize the ValidFeedback.

        Raises:
            RangeError: If the number_of_dots parameter is not in valid range.
        """
        NumberOfDots().validate_value(self.number_of_dots)

    def validate_value(self, value: Any) -> Tuple[int, int]:
        """
        Validates the given feedback and returns the validated feedback.

        Args:
            value (Any): The feedback to be validated.

        Returns:
            Tuple[int, int]: The validated feedback.

        Raises:
            InputConversionError: If the input cannot be converted a tuple of integers.
            TypeValidationError: If the feedback is not a tuple of two integers.
            RangeError: If the feedback values are not within the valid range.
        """
        if isinstance(value, str):
            value = self.convert(value)

        if not isinstance(value, (tuple, list)):
            raise TypeValidationError(
                "Feedback must be a tuple or list of two integers"
            )

        if len(value) != 2:
            raise RangeError("Feedback must be a tuple of two integers")

        if sum(value) > self.number_of_dots:
            raise RangeError(f"Feedback values sum cannot exceed {self.number_of_dots}")

        _GameValidationUtils.validate_integer_range(value, 0, self.number_of_dots)

        return value
