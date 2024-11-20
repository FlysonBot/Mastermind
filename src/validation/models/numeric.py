from src.validation.base import ConstrainedInteger


class NumberOfDots(ConstrainedInteger):
    """Validates number of dots."""

    def __init__(self) -> None:
        super().__init__(ge=2)


class NumberOfColors(ConstrainedInteger):
    """Validates number of colors."""

    def __init__(self) -> None:
        super().__init__(ge=2)


class NumberOfGuessesMade(ConstrainedInteger):
    """Validates number of guesses made."""

    def __init__(self) -> None:
        super().__init__(ge=0)


class MaximumAttempts(ConstrainedInteger):
    """Validates maximum attempts allowed."""

    def __init__(self) -> None:
        super().__init__(ge=1)
