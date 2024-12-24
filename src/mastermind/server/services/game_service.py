from mastermind.database import Game, get_winner
from mastermind.server.services.gameboard_service import GameboardService


class GameEndedException(Exception):
    pass


class GameNotStartedException(Exception):
    pass


class GameService:
    def __init__(self, game: Game) -> None:
        """Initializes a new game service with the given game.

        Args:
            game (Game): The game to be managed.
        """

        self._game_board = game.game_board
        self._game_configuration = game.game_configuration
        self._game_entities = game.game_entities
        self._game_state = game.game_state
        self._gameboard_service = GameboardService(self._game_board)

    def add_round(self, guess: tuple[int, ...], feedback: tuple[int, int]) -> None:
        """Adds a new game round with the player's guess and corresponding feedback.

        Appends the round to game rounds and clears the undo stack to prevent branching.
        This method should be called from the GameController, not directly by the player.

        Args:
            guess (tuple[int, ...]): A tuple representing the player's current guess.
            feedback (tuple[int, int]): A tuple containing the number of correct and misplaced pegs.

        Raises:
            GameEndedException: When trying to add a round to a game that has ended.
        """

        if self._game_state.game_over:
            raise GameEndedException("Cannot add round to game that has ended.")

        self._gameboard_service.add_round(guess, feedback)
        self._game_state.game_started = True
        self._game_state.winner = get_winner(
            num_attempts=len(self._game_board),
            max_attempts=self._game_configuration.ATTEMPTS_ALLOWED,
            last_feedback=self._gameboard_service.game_rounds[-1].FEEDBACK,
            number_of_dots=self._game_configuration.NUMBER_OF_DOTS,
        )

    def undo(self) -> None:
        """Undo the most recent game round.

        Raises:
            GameNotStartedException: When trying to undo game rounds before the game has started.
            GameEndedException: When trying to undo game rounds after the game has ended.
        """

        if not self._game_state.game_started:
            raise GameNotStartedException(
                "Cannot undo game rounds before game has started."
            )

        if self._game_state.game_over:
            raise GameEndedException("Cannot undo game rounds after game has ended.")

        self._gameboard_service.undo()

    def redo(self) -> None:
        """Restores the most recently undone game round.

        Raises:
            GameNotStartedException: When trying to redo game rounds before the game has started.
        """

        if not self._game_state.game_started:
            raise GameNotStartedException(
                "Cannot redo game rounds before game has started."
            )

        self._gameboard_service.redo()