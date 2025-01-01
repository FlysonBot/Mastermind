from enum import Enum

from mastermind.libs.utils import serialize_enum_name_only
from mastermind.server.players import (
    ComputerBreaker,
    ComputerSetter,
    EnvironmentBreaker,
    EnvironmentSetter,
    HumanBreaker,
    HumanSetter,
)


@serialize_enum_name_only
class GameMode(Enum):
    """Enum for the different game modes, which determined who is Player 1 (Code Setter) and who is Player 2 (Code Breaker).

    Members:
        PVP: Both players are Humans (user input for both players if played locally).
        PVC: Player 1 is a Human (user), Player 2 is a Computer.
        CVP: Player 1 is a Computer, Player 2 is a Human (user).
        EVE: Both players are Environments (user input for both players).
    """

    PVP = (HumanSetter, HumanBreaker)
    PVC = (HumanSetter, ComputerBreaker)
    CVP = (ComputerSetter, HumanBreaker)
    EVE = (EnvironmentSetter, EnvironmentBreaker)
