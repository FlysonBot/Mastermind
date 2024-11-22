from src.validation.base import ConstrainedInteger


class NumberOfDots(ConstrainedInteger):
    """
    A ConstrainedInteger that validates the number of dots in the game.

    The number of dots must be greater than or equal to 2.
    """

    def __init__(self) -> None:
        super().__init__(ge=2)


class NumberOfColors(ConstrainedInteger):
    """
    A ConstrainedInteger that validates the number of colors in the game.

    The number of colors must be greater than or equal to 2.
    """

    def __init__(self) -> None:
        super().__init__(ge=2)


class NumberOfGuessesMade(ConstrainedInteger):
    """
    A ConstrainedInteger that validates the number of guesses made in the game.

    The number of guesses must be greater than or equal to 0.
    """

    def __init__(self) -> None:
        super().__init__(ge=0)


class MaximumAttempts(ConstrainedInteger):
    """
    A ConstrainedInteger that validates the maximum number of attempts allowed in the game.

    The maximum number of attempts must be greater than or equal to 1.
    """

    def __init__(self) -> None:
        super().__init__(ge=1)
