from collections import deque
from random import randint
from typing import Any, Optional, Tuple

from .players import *
from .utils import get_feedback, Stack
from .validation import *


class Game(BaseModel):
    """A class to represent a Mastermind game."""

    # Board subclass to store board status
    class _Board(BaseModel):
        """A class to represent a Mastermind board with guesses and feedbacks."""

        class EmptyBoardError(Exception):
            """Custom exception for empty board."""

            pass

        def __init__(self, number_of_colors: int, number_of_dots: int) -> None:
            """Initializes the board."""
            self.NUMBER_OF_COLORS = number_of_colors
            self.NUMBER_OF_DOTS = number_of_dots
            self._number_of_guesses_made = 0
            self._guesses = Stack()
            self._feedbacks = Stack()

        def __len__(self) -> int:
            """Returns the number of guesses made."""
            return self._number_of_guesses_made

        def __getitem__(self, index: int) -> Tuple:
            """Returns the guess and feedback at the given index."""
            return self._guesses[index], self._feedbacks[index]

        def last_guess(self) -> Tuple:
            """Returns the last guess."""
            if self._number_of_guesses_made == 0:
                raise self.EmptyBoardError("No guesses to return.")
            return self._guesses.top()

        def last_feedback(self) -> Tuple:
            """Returns the last feedback."""
            if self._number_of_guesses_made == 0:
                raise self.EmptyBoardError("No guesses to return.")
            return self._feedbacks.top()

        def remove_last(self) -> Tuple:
            """Undoes the last guess and its feedback."""
            if self._number_of_guesses_made == 0:
                raise self.EmptyBoardError("No guesses to remove.")
            guess = self._guesses.pop()
            feedback = self._feedbacks.pop()
            self._number_of_guesses_made -= 1
            return guess, feedback

        def add_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
            """Adds a guess and its feedback to the board."""
            ValidGuess(
                guess,
                number_of_dots=self.NUMBER_OF_DOTS,
                number_of_colors=self.NUMBER_OF_COLORS,
            )
            ValidFeedback(feedback, number_of_dots=self.NUMBER_OF_DOTS)
            self._guesses.push(guess)
            self._feedbacks.push(feedback)
            self._number_of_guesses_made += 1

        def clear(self) -> None:
            """Clears the board."""
            self._guesses.clear()
            self._feedbacks.clear()
            self._number_of_guesses_made = 0

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
        self._board = self._Board(number_of_colors, number_of_dots)
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
        """Submits a guess and updates the board."""
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
            return None

        last_guess, last_feedback = (
            self._board.last_guess(),
            self._board.last_feedback(),
        )

        if hasattr(self, "SECRET_CODE") and last_guess == self.SECRET_CODE:
            self._win_status = True
            return True

        elif last_feedback == (self.number_of_dots, 0):
            self._win_status = True
            return True

        elif len(self._board) == self.MAXIMUM_ATTEMPTS:
            self._win_status = False
            return False

        return self._win_status  # Game continued

    def find_players(self) -> None:
        """Find suitable players for a game based on the game mode."""
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
        """Call players to obtain guess and feedback."""
        while self.win_status is None:
            # Obtain guess or command
            guess = self.PLAYER_CRACKER.obtain_guess()

            # Process commands
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

            # Get feedback
            feedback = self.PLAYER_SETTER.get_feedback(guess)

            # Process command
            if feedback == "q":  # quit
                break
            if feedback == "d":  # discard
                break
            if feedback == "u":  # undo
                continue  # since guess haven't been submitted, skip = undo

            # Submit guess
            self.submit_guess(guess, feedback)
            self.update_win_status()

    def output_result(self) -> None:
        """Output the result of the game."""
        self.update_win_status()
        if self.win_status is None:
            return
        if self.win_status:
            self.PLAYER_CRACKER.win_message()
        else:
            self.PLAYER_CRACKER.lose_message()

    # Game Flow Logic
    def start_game(self) -> Optional[str]:
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
