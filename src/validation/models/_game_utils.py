from typing import Tuple

from src.validation.base import (
    InputConversionError,
    RangeError,
    TypeValidationError,
)
from src.validation.models.numeric import NumberOfColors, NumberOfDots


class GameValidationUtils:
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
            raise InputConversionError("Invalid input format") from e

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
                raise TypeValidationError("Input must be consist of integers")

            if value < low_limit or value > high_limit:
                raise RangeError(
                    f"Value {value} is not in range [{low_limit}, {high_limit}]"
                )
