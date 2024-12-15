from enum import Enum

from mastermind.core.controllers.players import Player


class GameMode(Enum):
    """Enum for the different game modes, which determined who is Player 1 and who is Player 2.

    Members:
        PVP: Player versus player mode.
        PVE: Player versus environment mode.
        EVP: Environment versus player mode.
        EVE: Environment versus environment mode.
    """

    # placeholder for concrete players
    PVP = (Player, Player)
    PVE = (Player, Player)
    EVP = (Player, Player)
    EVE = (Player, Player)
