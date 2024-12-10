from dataclasses import dataclass
from typing import Deque

from mastermind.core.models.game_round import GameRound


@dataclass
class GameBoard:
    """
    Dataclass for the gameboard of a game.

    This class represents the collection of game rounds that have taken place during a game session. It serves as a structured way to manage and track the progression of the game through its various rounds.

    Attributes:
        game_rounds (Deque[GameRound]): A collection of GameRound instances, each representing a round of the game.
    """

    game_rounds: Deque[GameRound]
