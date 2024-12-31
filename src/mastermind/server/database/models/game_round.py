from typing import Optional, Tuple

from attrs import frozen


@frozen
class GameRound:
    """for a single round of the game.

    This class encapsulates the guess made during a round and the corresponding feedback received.

    Attributes:
        GUESS (Tuple[int, ...]): A tuple representing the player's guess.
        FEEDBACK (Tuple[int, int]): A tuple containing feedback information, typically indicating the number of correct guesses and their positions.

    Examples:
        >>> round = GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(2, 1), NUMBER_OF_COLORS=6, NUMBER_OF_DOTS=4)
        >>> round
        GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(2, 1))
        >>> round.FEEDBACK
        (2, 1)
        >>> round.NUMBER_OF_COLORS
        Traceback (most recent call last):
        ...
        AttributeError: 'GameRound' object has no attribute 'NUMBER_OF_COLORS'
    """

    GUESS: Tuple[int, ...]
    FEEDBACK: Tuple[int, int]

    def __init__(
        self,
        GUESS: Tuple[int, ...],
        FEEDBACK: Tuple[int, int],
        NUMBER_OF_COLORS: Optional[int] = None,
        NUMBER_OF_DOTS: Optional[int] = None,
    ) -> None:
        if NUMBER_OF_COLORS and NUMBER_OF_DOTS:
            _validate_guess(GUESS, NUMBER_OF_COLORS, NUMBER_OF_DOTS)
            _validate_feedback(FEEDBACK, NUMBER_OF_DOTS)

        self.__attrs_init__(GUESS, FEEDBACK)  # type: ignore

    def validate(self, NUMBER_OF_COLORS: int, NUMBER_OF_DOTS: int) -> None:
        """Validate the round based on the number of colors and dots.

        Args:
            NUMBER_OF_COLORS (int): The number of colors available to a code.
            NUMBER_OF_DOTS (int): The number of dots in each code.

        Examples:
            >>> round = GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(2, 1), NUMBER_OF_COLORS=6, NUMBER_OF_DOTS=4)
            >>> round.validate(NUMBER_OF_COLORS=6, NUMBER_OF_DOTS=4)
        """
        _validate_guess(self.GUESS, NUMBER_OF_COLORS, NUMBER_OF_DOTS)
        _validate_feedback(self.FEEDBACK, NUMBER_OF_DOTS)


def _validate_guess(
    guess: Tuple[int, ...], NUMBER_OF_COLORS: int, NUMBER_OF_DOTS: int
) -> None:
    """
    Examples:
        >>> GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(2, 1), NUMBER_OF_COLORS=3, NUMBER_OF_DOTS=4)
        Traceback (most recent call last):
        ...
        ValueError: Guess must contain only numbers between 1 and 3 (the number of colors).

        >>> GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(2, 1), NUMBER_OF_COLORS=6, NUMBER_OF_DOTS=3)
        Traceback (most recent call last):
        ...
        ValueError: Guess must be of length 3 (the number of dots).

        >>> GameRound(GUESS=(1, 2, 3, 4, 5), FEEDBACK=(2, 1), NUMBER_OF_COLORS=6, NUMBER_OF_DOTS=4)
        Traceback (most recent call last):
        ...
        ValueError: Guess must be of length 4 (the number of dots).
    """
    if len(guess) != NUMBER_OF_DOTS:
        raise ValueError(
            f"Guess must be of length {NUMBER_OF_DOTS} (the number of dots)."
        )

    if not all(1 <= dot <= NUMBER_OF_COLORS for dot in guess):
        raise ValueError(
            f"Guess must contain only numbers between 1 and {NUMBER_OF_COLORS} (the number of colors)."
        )


def _validate_feedback(feedback: Tuple[int, int], NUMBER_OF_DOTS: int) -> None:
    """
    Examples:
        >>> GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(2, 1, 2), NUMBER_OF_COLORS=6, NUMBER_OF_DOTS=4)
        Traceback (most recent call last):
        ...
        ValueError: Feedback must be of length 2

        >>> GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(-1, 1), NUMBER_OF_COLORS=6, NUMBER_OF_DOTS=4)
        Traceback (most recent call last):
        ...
        ValueError: Feedback cannot contain negative numbers.
    """
    if len(feedback) != 2:
        raise ValueError("Feedback must be of length 2")

    if sum(feedback) > NUMBER_OF_DOTS:
        raise ValueError(
            f"Sum of feedback cannot possibly be greater than {NUMBER_OF_DOTS} (the number of dots)."
        )

    if any(dot < 0 for dot in feedback):
        raise ValueError("Feedback cannot contain negative numbers.")
