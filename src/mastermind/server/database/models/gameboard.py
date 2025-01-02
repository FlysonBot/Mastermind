from collections import deque
from typing import Deque, Generator, Tuple

from attrs import Factory, frozen

from .game_round import GameRound


@frozen  # Just the reference, game_rounds is still mutable
class GameBoard:
    """Dataclass for the gameboard of a game.

    This class represents the collection of game rounds that have taken place during a game session. It serves as a structured way to manage and track the progression of the game through its various rounds.

    Attributes:
        game_rounds (Deque[GameRound]): A collection of GameRound instances, each representing a round of the game.
    """

    game_rounds: Deque[GameRound] = Factory(deque)

    def __len__(self) -> int:
        """Returns the number of game rounds in the game board.

        Returns:
            int: Number of game rounds in the game board.

        Examples:
            >>> game_board = GameBoard(game_rounds=[GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0)), GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))])
            >>> len(game_board)
            2
        """
        return len(self.game_rounds)

    @property
    def guesses(self) -> Generator[Tuple[int, ...], None, None]:
        """Returns a generator of all guesses made in the game to allow for easy iteration.

        Returns:
            Generator[Tuple[int, ...], None, None]: A generator of all guesses made in the game.

        Examples:
            >>> game_board = GameBoard(game_rounds=[GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0)), GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))])
            >>> for guess in game_board.guesses:
            ...     print(guess)
            (1, 2, 3, 4)
            (3, 4, 5, 6)
        """
        return (round.GUESS for round in self.game_rounds)

    @property
    def feedbacks(self) -> Generator[Tuple[int, int], None, None]:
        """Returns a generator of all feedbacks received in the game to allow for easy iteration.

        Yields:
            Generator[Tuple[int], None, None]: A generator of all feedbacks received in the game.

        Examples:
            >>> game_board = GameBoard(game_rounds=[GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0)), GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))])
            >>> for feedback in game_board.feedbacks:
            ...     print(feedback)
            (1, 0)
            (2, 1)
        """
        return (round.FEEDBACK for round in self.game_rounds)

    def validate_all_rounds(self, NUMBER_OF_COLORS: int, NUMBER_OF_DOTS: int) -> None:
        """Validate all rounds in the game board.

        Args:
            NUMBER_OF_COLORS (int): The number of colors available to a code.
            NUMBER_OF_DOTS (int): The number of dots in each code.
        """
        for round in self.game_rounds:
            round.validate(NUMBER_OF_COLORS, NUMBER_OF_DOTS)
