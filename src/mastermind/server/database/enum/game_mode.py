from mastermind.libs.utils import EnumMeta, serialize_enum_name_only
from mastermind.server.players import Player


@serialize_enum_name_only
class GameMode(EnumMeta):
    """Enum for the different game modes, which determined who is Player 1 and who is Player 2.

    Members:
    """

    # placeholder for concrete players
    PVP = (Player, Player)
    PVC = (Player, Player)
    CPV = (Player, Player)
    EVE = (Player, Player)
