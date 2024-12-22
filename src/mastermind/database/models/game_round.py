from dataclasses import dataclass
from typing import Tuple

from mastermind.utils import DataClassJson


@dataclass(frozen=True)
class GameRound(DataClassJson):
    """for a single round of the game.

    This class encapsulates the guess made during a round and the corresponding feedback received.

    Attributes:
        GUESS (Tuple[int, ...]): A tuple representing the player's guess.
        FEEDBACK (Tuple[int, int]): A tuple containing feedback information, typically indicating the number of correct guesses and their positions.

    Examples:
        >>> round = GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(2, 1))
        >>> print(round.GUESS)
        (1, 2, 3, 4)
        >>> print(round.FEEDBACK)
        (2, 1)
    """

    GUESS: Tuple[int, ...]
    FEEDBACK: Tuple[int, int]
