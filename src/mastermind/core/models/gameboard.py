from dataclasses import dataclass
from typing import List

from mastermind.core.models.game_round import GameRound


@dataclass
class GameBoard:
    """Dataclass for the gameboard of a game."""

    game_rounds: List[GameRound]
