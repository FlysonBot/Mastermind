from typing import Optional, Tuple

from src.game.board import GameBoard
from src.players import (
    AICracker,
    AISetter,
    ExternalSetter,
    HumanCracker,
    HumanSetter,
)
from src.validation import BaseModel, Booleans, TrueFuse


class _Utils:
    @staticmethod
    def last_guess_is_secret(game: "Game") -> bool:
        return (
            hasattr(game, "SECRET_CODE")
            and game._board.last_guess() == game.SECRET_CODE
        )

    @staticmethod
    def last_feedback_is_perfect(game: "Game") -> bool:
        return game._board.last_feedback() == (game.number_of_dots, 0)

    @staticmethod
    def reached_maximum_attempts(game: "Game") -> bool:
        return len(game._board) == game.MAXIMUM_ATTEMPTS


class Game(BaseModel):
    """
    A class to represent a Mastermind game, managing the game state and player interactions.

    This class initializes the game with specified parameters and handles the game flow,
    including submitting guesses, updating win status, and managing players based on the game mode.

    Args:
        number_of_colors (int): The number of colors available for guesses.
        number_of_dots (int): The number of dots in each guess.
        maximum_attempts (int): The maximum number of attempts allowed for the game.
        game_mode (str): The mode of the game, determining the type of players involved.

    Attributes:
        number_of_colors (int): The number of colors available for guesses.
        number_of_dots (int): The number of dots in each guess.
        win_status (Optional[bool]): The current win status of the game, if determined.
        game_started (bool): Indicates whether the game has started.

    Examples:
        game = Game(number_of_colors=6, number_of_dots=4, maximum_attempts=10, game_mode='HvH')
        game.start_game()
    """

    # Initialization
    def __init__(
        self,
        number_of_colors: int,
        number_of_dots: int,
        maximum_attempts: int,
        game_mode: str,
    ) -> None:
        """Initializes the game."""
        self.MAXIMUM_ATTEMPTS = maximum_attempts
        self.GAME_MODE = game_mode
        self._board = GameBoard(number_of_colors, number_of_dots)
        self._game_started = TrueFuse(False)
        self._win_status = Booleans(None)

    # Accessors
    @property
    def number_of_colors(self) -> int:
        return self._board.NUMBER_OF_COLORS

    @property
    def number_of_dots(self) -> int:
        return self._board.NUMBER_OF_DOTS

    @property
    def win_status(self) -> Optional[bool]:
        return self._win_status

    @property
    def game_started(self) -> bool:
        return self._game_started

    def __len__(self) -> int:
        return len(self._board)

    # Mutators
    def submit_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
        """
        Submits a player's guess and updates the game board with the corresponding feedback.

        This function checks if the game is still ongoing and if the maximum number of
        attempts has not been reached before adding the guess and feedback to the board.
        It also clears any undo actions for both the guesser and the setter.
        """
        if self._win_status is not None:
            raise NotImplementedError("Cannot make guess after game has ended.")
        if len(self._board) >= self.MAXIMUM_ATTEMPTS:
            raise NotImplementedError(
                "Cannot make guess after maximum attempts reached."
            )
        self.PLAYER_CRACKER.clear_undo()
        self.PLAYER_SETTER.clear_undo()
        self._board.add_guess(guess, feedback)

    def update_win_status(self) -> Optional[bool]:
        """Updates the win status of the game."""
        if len(self._board) == 0:
            self._win_status = None

        if _Utils.last_guess_is_secret(self):
            self._win_status = True

        elif _Utils.last_feedback_is_perfect(self):
            self._win_status = True

        elif _Utils.reached_maximum_attempts(self):
            self._win_status = False

        # When non of the above is true, game continues
        return self._win_status

    def find_players(self) -> None:
        """Determines and assigns players based on the game mode."""
        if self.GAME_MODE == "HvH":
            self.PLAYER_CRACKER = HumanCracker(self)
            self.PLAYER_SETTER = HumanSetter(self)
        elif self.GAME_MODE == "HvAI":
            self.PLAYER_CRACKER = HumanCracker(self)
            self.PLAYER_SETTER = AISetter(self)
        elif self.GAME_MODE == "AIvH":
            self.PLAYER_CRACKER = AICracker(self)
            self.PLAYER_SETTER = HumanSetter(self)
        else:
            self.PLAYER_CRACKER = AICracker(self)
            self.PLAYER_SETTER = ExternalSetter(self)

    def player_guessing_logic(self) -> Optional[str]:
        """Handle the logic for player guessing."""
        while self.win_status is None:
            # Obtain guess or command from cracker player
            guess = self.PLAYER_CRACKER.obtain_guess()

            # Process commands from cracker player
            if guess == "q":  # quit
                return "q"
            if guess == "d":  # discard
                return "d"
            if guess == "u":  # undo
                self.PLAYER_CRACKER.undo()
                self.PLAYER_SETTER.undo()
                self._board.remove_last()
                continue
            if guess == "r":  # redo
                guess = self.PLAYER_CRACKER.redo()
                feedback = self.PLAYER_SETTER.redo()
                self.submit_guess(guess, feedback)
                continue

            # Get feedback from setter player
            feedback = self.PLAYER_SETTER.get_feedback(guess)

            # Process command from setter player
            if feedback == "q":  # quit
                break
            if feedback == "d":  # discard
                break
            if feedback == "u":  # undo
                continue  # since guess haven't been submitted, skip = undo

            # Submit guess and feedback
            self.submit_guess(guess, feedback)
            self.update_win_status()

    def output_result(self) -> None:
        """Print the result of the game."""
        self.update_win_status()
        if self.win_status is None:
            return
        if self.win_status:
            self.PLAYER_CRACKER.win_message()
        else:
            self.PLAYER_CRACKER.lose_message()

    # Game Flow Logic
    def start_game(self) -> Optional[str]:  # sourcery skip: class-extract-method
        """Starts the game."""
        # Check Condition
        if self._game_started:
            raise NotImplementedError("Game has already started.")

        # Start Game
        self._game_started = True
        self.find_players()
        self.PLAYER_SETTER.set_secret_code()

        command = self.player_guessing_logic()  # Handle player actions

        # Post-termination Logic
        self.output_result()
        return command

    def resume_game(self) -> None:
        """Resumes the game."""
        # Check Condition
        if not self._game_started:
            raise NotImplementedError("Game has not started yet.")

        command = self.player_guessing_logic()  # Handle player actions

        # Post-termination Logic
        self.output_result()
        return command
