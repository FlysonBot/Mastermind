from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..database.enum.player_role import PlayerRole

Combination = tuple[int, ...]
Feedback = tuple[int, int]


@dataclass
class Player:
    client_id: str
    player_role: PlayerRole = PlayerRole.UNDETERMINED

    def __repr__(self) -> str:
        return "Player()"


class CodeSetter(ABC, Player):
    player_role = PlayerRole.CODE_SETTER

    @abstractmethod
    def obtain_feedback(self) -> Feedback:
        pass


class CodeBreaker(ABC, Player):
    player_role = PlayerRole.CODE_BREAKER

    @abstractmethod
    def obtain_guess(self) -> Combination:
        pass
