from mastermind.client.languages import global_localization
from mastermind.libs.logs import ServerLogger
from mastermind.server.database.models import Game, get_winner
from mastermind.server.services.gameboard_service import GameboardService

game_service = global_localization.services.game_service
logger = ServerLogger("GameService")


class GameEndedException(Exception):
    pass


class GameNotStartedException(Exception):
    pass


class GameService:
    def __init__(self, game: Game, gameboard_service: GameboardService) -> None:
        """Initializes a new game service with the given game.

        Args:
            game (Game): The game to be managed.
        """

        self._game_board = game.game_board
        self._game_configuration = game.game_configuration
        self._game_entities = game.game_entities
        self._game_state = game.game_state
        self._gameboard_service = gameboard_service

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

        logger.debug(
            f"Adding round to game with guess: {guess} and feedback: {feedback}"
        )
        if self._game_state.game_over:
            self.warn_state("Attempted to add round to game that has ended")
            raise GameEndedException(game_service.game_ended_add_round)

        self._gameboard_service.add_round(guess, feedback)
        self._game_state.game_started = True
        self._game_state.winner = get_winner(
            num_attempts=len(self._game_board),
            max_attempts=self._game_configuration.ATTEMPTS_ALLOWED,
            last_feedback=self._gameboard_service.game_rounds[-1].FEEDBACK,
            number_of_dots=self._game_configuration.NUMBER_OF_DOTS,
        )
        self.inform_action("Add round successful")

    def undo(self) -> None:
        """Undo the most recent game round.

        Raises:
            GameNotStartedException: When trying to undo game rounds before the game has started.
            GameEndedException: When trying to undo game rounds after the game has ended.
        """

        logger.debug("Attempting to undo game round")
        if not self._game_state.game_started:
            self.warn_state("Attempted to undo game round before game has started")
            raise GameNotStartedException(game_service.game_not_started_undo)

        if self._game_state.game_over:
            self.warn_state("Attempted to undo game round after game has ended")
            raise GameEndedException(game_service.game_ended_undo)

        self._gameboard_service.undo()
        self.inform_action("Undo successful")

    def redo(self) -> None:
        """Restores the most recently undone game round.

        Raises:
            GameNotStartedException: When trying to redo game rounds before the game has started.
        """

        logger.debug("Attempting to redo game round")
        if not self._game_state.game_started:
            self.warn_state("Attempted to redo game round before game has started")
            raise GameNotStartedException(game_service.game_not_started_redo)

        self._gameboard_service.redo()
        self.inform_action("Redo successful")

    def inform_action(self, message: str) -> None:
        logger.info(message)
        state_message = f"Game state: {self._game_state}"
        state_message += f"Game rounds: {self._gameboard_service.game_rounds}"
        state_message += f"Undo stack: {self._gameboard_service.undo_stack}"
        logger.debug(state_message)

    def warn_state(self, message: str) -> None:
        logger.warning(message)
        logger.debug(f"Game state: {self._game_state}")
