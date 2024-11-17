from typing import Optional, Tuple

from main.players import (
    AICracker,
    AISetter,
    ExternalSetter,
    HumanCracker,
    HumanSetter,
)
from main.utils import Stack
from main.validation import (
    BaseModel,
    Booleans,
    TrueFuse,
    ValidFeedback,
    ValidGuess,
)


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

    # Board subclass to store board status
    class _Board(BaseModel):
        """
        A class to represent a Mastermind game board, storing guesses and feedback.

        This class manages the state of the game board, including adding guesses, retrieving the last guess and feedback, and handling the number of guesses made.

        Args:
            number_of_colors (int): The number of colors available for guesses.
            number_of_dots (int): The number of dots in each guess.

        Raises:
            EmptyBoardError: If an operation is attempted on an empty board.

        Examples:
            board = _Board(number_of_colors=6, number_of_dots=4)
            board.add_guess((1, 2, 3, 4), (1, 0))
            last_guess = board.last_guess()
        """


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
        """Handle the lgoci for player guessing."""
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
