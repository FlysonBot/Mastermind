from dataclasses import dataclass

from mastermind.utils import EnumMeta, serialize_enum_name_only


@dataclass
class Player:
    def __repr__(self) -> str:
        return "Player()"


@serialize_enum_name_only
class PlayerRole(EnumMeta):
    CODE_SETTER = "CODE_SETTER"
    CODE_BREAKER = "CODE_BREAKER"
    UNDETERMINED = "UNDETERMINED"
