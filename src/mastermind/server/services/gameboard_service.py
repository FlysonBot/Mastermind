from collections import deque
from typing import Deque

from mastermind.client.languages import global_localization
from mastermind.libs.logs import ServerLogger

from ..database.models import GameRound, GameBoard

gameboard_service = global_localization.services.gameboard_service
logger = ServerLogger("GameboardService")


class NoUndoAvailableException(Exception):
    pass


class NoRedoAvailableException(Exception):
    pass


class GameboardService:
    """This class manages the game board and provides methods for adding and undoing game rounds.

    It should be called from the GameService, not directly by the player.

    Attributes:
        game_rounds (Deque[GameRound]): A deque of GameRound instances, each representing a round of the game.
        undo_stack (Deque[GameRound]): A deque of GameRound instances, representing the undo stack.
    """

    def __init__(self, gameboard: GameBoard) -> None:
        """Initializes a new game board service with the current game board state.

        The service prepares game rounds and an undo stack for tracking game progress.

        Args:
            gameboard (GameBoard): The current game board to be managed.
        """

        self.game_rounds: Deque[GameRound] = gameboard.game_rounds
        self.undo_stack: Deque[GameRound] = deque()

    def undo(self) -> None:
        """Removes the most recent game round and stores it in the undo stack.

        Allows players to undo their most recent game round and return to a previous state.

        Examples:
            >>> gameboard = GameBoard(game_rounds=[GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0)), GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))])
            >>> service = GameboardService(gameboard)
            >>> service.game_rounds
            [GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0)), GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))]
            >>> service.undo()
            >>> service.game_rounds
            [GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0))]
        """

        logger.debug("Attempting to undo game round")

        try:
            self.undo_stack.append(self.game_rounds.pop())
        except IndexError as e:
            logger.warning("No more game rounds to undo")
            raise NoUndoAvailableException(gameboard_service.no_undo_available) from e

        self.inform_action("Undo successful")

    def redo(self) -> None:
        """Restores the most recently undone game round from the undo stack.

        Allows players to reapply a previously undone game round.

        Examples:
            >>> gameboard = GameBoard(game_rounds=[GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0)), GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))])
            >>> service = GameboardService(gameboard)
            >>> service.game_rounds
            [GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0)), GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))]
            >>> service.undo()
            >>> service.redo()
            >>> service.game_rounds
            [GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0)), GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))]
        """

        logger.debug("Attempting to redo game round")

        try:
            self.game_rounds.append(self.undo_stack.pop())
        except IndexError as e:
            logger.warning("No more game rounds to redo")
            raise NoRedoAvailableException(gameboard_service.no_redo_available) from e

        self.inform_action("Redo successful")

    def add_round(self, guess: tuple[int, ...], feedback: tuple[int, int]) -> None:
        """Adds a new game round with the player's guess and corresponding feedback.

        Appends the round to game rounds and clears the undo stack to prevent branching.

        Args:
            guess (tuple[int, ...]): A tuple representing the player's current guess.
            feedback (tuple[int, int]): A tuple containing the number of correct and misplaced pegs.

        Examples:
            >>> gameboard = GameBoard(game_rounds=[GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1))])
            >>> service = GameboardService(gameboard)
            >>> service.add_round((1, 2, 3, 4), (1, 0))
            >>> service.game_rounds
            [GameRound(GUESS=(3, 4, 5, 6), FEEDBACK=(2, 1)), GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0))]
        """

        logger.debug(
            f"Adding round to game with guess: {guess} and feedback: {feedback}"
        )
        self.game_rounds.append(GameRound(GUESS=guess, FEEDBACK=feedback))
        self.undo_stack.clear()
        self.inform_action("Add round successful")

    def inform_action(self, message: str) -> None:
        logger.info(message)
        logger.debug(f"Game rounds: {self.game_rounds}")
        logger.debug(f"Undo stack: {self.undo_stack}")
