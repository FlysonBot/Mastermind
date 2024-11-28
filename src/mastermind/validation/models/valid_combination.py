from typing import Any, Tuple

from mastermind.validation.base import (
    RangeError,
    TypeValidationError,
    ValidationModel,
)
from mastermind.validation.models._game_utils import GameValidationUtils


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
        self.convert = lambda value: GameValidationUtils.convert(value)
        self.validate_arguments = lambda: GameValidationUtils.validate_arguments(self)
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

        GameValidationUtils.validate_integer_range(value, 1, self.n_of_colors)

        return tuple(value)
