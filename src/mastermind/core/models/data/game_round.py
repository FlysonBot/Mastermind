from dataclasses import dataclass
from typing import Tuple


@dataclass
class GameRound:
    """Dataclass for a single round of the game."""

    guess: Tuple[int, ...]
    feedback: Tuple[int, int]
