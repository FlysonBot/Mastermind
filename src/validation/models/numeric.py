from src.validation.base import ConstrainedInteger


class NumberOfDots(ConstrainedInteger):
    def __init__(self) -> None:
        super().__init__(ge=2)


class NumberOfColors(ConstrainedInteger):
    def __init__(self) -> None:
        super().__init__(ge=2)


class NumberOfGuessesMade(ConstrainedInteger):
    def __init__(self) -> None:
        super().__init__(ge=0)


class MaximumAttempts(ConstrainedInteger):
    def __init__(self) -> None:
        super().__init__(ge=1)
