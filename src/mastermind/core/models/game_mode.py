from enum import Enum


class GameMode(Enum):
    """
    Enum for the different game modes, which determined who is Player 1 and who is Player 2.

    Members:
        PVP: Player versus player mode.
        PVE: Player versus environment mode.
        EVP: Environment versus player mode.
        EVE: Environment versus environment mode.
    """

    PVP = ()  # place implemented player class here
    PVE = ()  # for example, (Player1, Player2)
    EVP = ()
    EVE = ()
