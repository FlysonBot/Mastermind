from mastermind.utils.enum_meta import EnumMeta


class Player:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def to_json(self) -> str:
        return "{}"

    @classmethod
    def from_json(cls, json_string: str) -> "Player":
        return cls()


class PlayerRole(EnumMeta):
    CODE_SETTER = "CODE_SETTER"
    CODE_BREAKER = "CODE_BREAKER"
