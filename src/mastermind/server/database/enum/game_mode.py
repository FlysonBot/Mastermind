from enum import Enum

from mastermind.server.players import Player
from mastermind.libs.utils import serialize_enum_name_only


@serialize_enum_name_only
class GameMode(Enum):
    """Enum for the different game modes, which determined who is Player 1 and who is Player 2.

    Members:
    """

    # placeholder for concrete players
    PVP = (Player, Player)
    PVC = (Player, Player)
    CPV = (Player, Player)
    EVE = (Player, Player)
