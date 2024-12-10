from dataclasses import dataclass

from mastermind.core.models.behavior.players import Player


@dataclass
class GameEntities:
    """Dataclass for the entities of a game (such as players or those from plugins)."""

    code_setter: Player
    code_breaker: Player
