from mastermind.utils.enum_meta import EnumMeta


class Player:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class PlayerRole(EnumMeta):
    CODE_SETTER = "CODE_SETTER"
    CODE_BREAKER = "CODE_BREAKER"
