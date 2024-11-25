from typing import Any, Tuple

from src.validation.base import (
    RangeError,
    TypeValidationError,
    ValidationModel,
)
from src.validation.models._game_utils import GameValidationUtils
from src.validation.models.numeric import NumberOfDots


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
        self.convert = lambda value: GameValidationUtils.convert(value)
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
            raise RangeError("Feedback must be a tuple or list of two integers")

        if sum(value) > self.number_of_dots:
            raise RangeError(f"Feedback values sum cannot exceed {self.number_of_dots}")

        GameValidationUtils.validate_integer_range(value, 0, self.number_of_dots)

        return value
