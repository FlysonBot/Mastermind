from dataclasses import dataclass
from typing import Tuple


@dataclass
class GameRound:
    """
    Dataclass for a single round of the game.

    This class encapsulates the guess made during a round and the corresponding feedback received.

    Attributes:
        guess (Tuple[int, ...]): A tuple representing the player's guess.
        feedback (Tuple[int, int]): A tuple containing feedback information, typically indicating the number of correct guesses and their positions.
    """

    guess: Tuple[int, ...]
    feedback: Tuple[int, int]
