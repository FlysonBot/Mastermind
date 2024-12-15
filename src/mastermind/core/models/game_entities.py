from dataclasses import dataclass

from mastermind.core.controllers.players import Player
from mastermind.core.models.game_mode import GameMode


@dataclass(frozen=True)
class GameEntities:
    """Dataclass for the entities of a game (such as players or those from plugins).

    This class represents the key participants in a game, specifically the players involved in setting and breaking the code. It serves as a structured way to manage and reference these entities throughout the game's lifecycle.

    Attributes:
        CODE_SETTER (Player): The player responsible for setting the code.
        CODE_BREAKER (Player): The player tasked with breaking the code.
    """

    CODE_SETTER: Player
    CODE_BREAKER: Player

    @classmethod
    def from_game_mode(cls, game_mode: GameMode) -> "GameEntities":
        """Creates game entities based on the given game mode.

        Args:
            game_mode (GameMode): The game mode to create game entities for.

        Returns:
            GameEntities: The game entities based on the given game mode.

        Examples:
            >>> GameEntities.from_game_mode(GameMode.PVP)
            GameEntities(Player(), Player())
        """

        code_setter_class, code_breaker_class = game_mode.value
        return cls(code_setter_class(), code_breaker_class())

    def __repr__(self) -> str:
        return f"GameEntities({self.CODE_SETTER}, {self.CODE_BREAKER})"

