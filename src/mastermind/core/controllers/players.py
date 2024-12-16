from dataclasses import dataclass

from mastermind.utils import serialize_enum_name_only
from mastermind.utils.enum_meta import EnumMeta


@dataclass
class Player:
    def __repr__(self) -> str:
        return "Player()"


@serialize_enum_name_only
class PlayerRole(EnumMeta):
    CODE_SETTER = "CODE_SETTER"
    CODE_BREAKER = "CODE_BREAKER"
    UNDETERMINED = "UNDETERMINED"
