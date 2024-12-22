from dataclasses import dataclass

from mastermind.server import PlayerRole
from mastermind.utils import DataClassJson


@dataclass
class GameState(DataClassJson):
    """Dataclass for maintaining the current state of the game, indicating whether the game has started, if it is over, and who won.

    Attributes:
        game_started (bool): A flag indicating if the game has started.
        game_over (bool): A flag indicating if the game has ended.
        winner (PlayerRole): The player who won the game, if any. Only top level player (CodeSetter or Codebreaker) is allowed.
    """

    game_started: bool = False
    winner: PlayerRole = PlayerRole.UNDETERMINED

    @property
    def game_over(self) -> bool:
        """Returns a boolean indicating if the game has ended.

        Returns:
            bool: True if the game has ended, False otherwise.

        Examples:
            >>> game_state = GameState(game_started=True, winner=PlayerRole.UNDETERMINED)
            >>> game_state.game_over
            False
            >>> game_state = GameState(game_started=True, winner=PlayerRole.CODE_SETTER)
            >>> game_state.game_over
            True
        """
        return self.winner is not PlayerRole.UNDETERMINED


def get_winner(
    num_attempts: int,
    max_attempts: int,
    last_feedback: tuple[int, int],
    number_of_dots: int,
) -> PlayerRole:
    """Determines the winner of the game based on the number of attempts and the last feedback.

    Args:
        num_attempts (int): The number of attempts made by the player.
        max_attempts (int): The maximum number of attempts allowed.
        last_feedback (tuple[int, int]): The feedback received from the last game round.
        number_of_dots (int): The number of dots in the code.

    Returns:
        Optional[PlayerRole]: The winner of the game, if any.

    Examples:
        >>> get_winner(num_attempts=5, max_attempts=5, last_feedback=(1, 0), number_of_dots=4) == PlayerRole.CODE_SETTER
        True
        >>> get_winner(num_attempts=5, max_attempts=5, last_feedback=(4, 0), number_of_dots=4) == PlayerRole.CODE_BREAKER
        True
        >>> get_winner(num_attempts=4, max_attempts=5, last_feedback=(1, 0), number_of_dots=4) == PlayerRole.UNDETERMINED
        True
    """

    if last_feedback == (number_of_dots, 0):
        return PlayerRole.CODE_BREAKER

    return (
        PlayerRole.CODE_SETTER
        if num_attempts >= max_attempts
        else PlayerRole.UNDETERMINED
    )
