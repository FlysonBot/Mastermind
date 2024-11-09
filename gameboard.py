from .validation import BaseModel
from .utils import get_feedback
from collections import deque
from typing import Any, Optional, Tuple
from random import randint


class Stack:
    """An implementation of a stack data structure using deque."""
    
    def __init__(self, data: Optional[list] = None) -> None:
        """Initializes the stack."""
        self._stack = deque(data) if data else deque()

    def push(self, item: Any) -> None:
        """Adds an item to the top of the stack."""
        self._stack.append(item)

    def pop(self) -> Any:
        """Removes and returns the top item from the stack."""
        if self.is_empty():
            raise IndexError("No items to pop.")
        return self._stack.pop()

    def top(self) -> Any:
        """Returns the top item from the stack without removing it."""
        if self.is_empty():
            raise IndexError("No items to top.")
        return self._stack[-1]

    def is_empty(self) -> bool:
        """Returns True if the stack is empty, False otherwise."""
        return len(self._stack) == 0

    def __len__(self) -> int:
        """Returns the number of items in the stack."""
        return len(self._stack)

    def __getitem__(self, index: int) -> Any:
        """Returns the item at the given index counted from the top."""
        if index < 0 or index >= len(self._stack):
            raise IndexError("Index out of range.")
        return self._stack[-(index + 1)]

    def clear_stack(self) -> None:
        """Clears the stack."""
        self._stack.clear()

    @property
    def stack(self) -> list:
        """Returns the stack as a list. DO NOT EDIT THIS LIST."""
        return list(self._stack)

    def __iter__(self):
        """Return an iterator for the stack."""
        return iter(self._stack)


class Game(BaseModel):
    """A class to represent a Mastermind game."""
    
    # Board subclass to store board status
    class _Board(BaseModel):
        """A class to represent a Mastermind board. The board contain all
        the guesses made by a player and the feedback for each guess.
        """

        class EmptyBoardError(Exception):
            """Custom exception for empty board."""
            pass

        def __init__(self, number_of_colors: int, number_of_dots: int) -> None:
            """Initializes the board."""
            self.NUMBER_OF_COLORS = number_of_colors
            self.NUMBER_OF_DOTS = number_of_dots
            self._number_of_guesses_made = 0
            self._guesses = Constant(Stack())  # avoid modification to the reference
            self._feedbacks = Constant(Stack())  # stack is still modifiable

        def __len__(self) -> int:
            """Returns the number of guesses made."""
            return self._number_of_guesses_made
        
        def __getitem__(self, index: int) -> tuple:
            """Returns the guess and feedback at the given index."""
            return self._guesses[index], self._feedbacks[index]
        
        def last_guess(self) -> tuple:
            """Returns the last guess."""
            if self._number_of_guesses_made == 0:
                raise self.EmptyBoardError("No guesses to return.")
            return self._guesses.top()
        
        def last_feedback(self) -> tuple:
            """Returns the last feedback."""
            if self._number_of_guesses_made == 0:
                raise self.EmptyBoardError("No guesses to return.")
            return self._feedbacks.top()

        def remove_last(self) -> tuple:
            """Undoes the last guess and its feedback."""
            if self._number_of_guesses_made == 0:
                raise self.EmptyBoardError("No guesses to remove.")
            guess = self._guesses.pop()
            feedback = self._feedbacks.pop()
            self._number_of_guesses_made -= 1
            return guess, feedback

        def add_guess(self, guess: tuple, feedback: tuple) -> None:
            """Adds a guess and its feedback to the board."""
            ValidGuess(guess, number_of_dots=self.NUMBER_OF_DOTS, number_of_colors=self.NUMBER_OF_COLORS)
            ValidFeedback(feedback, number_of_dots=self.NUMBER_OF_DOTS)
            self._guesses.push(guess)
            self._feedbacks.push(feedback)
            self._number_of_guesses_made += 1

        def clear_board(self) -> None:
            """Clears the board."""
            self._guesses.clear_stack()
            self._feedbacks.clear_stack()
            self._number_of_guesses_made = 0


    # Initialization
    def __init__(self, number_of_colors: int, number_of_dots: int,
                 maximum_attempts: int, game_mode: str) -> None:
        """Initializes the game."""
        self.MAXIMUM_ATTEMPTS = maximum_attempts
        self.GAME_MODE = game_mode
        self._board = self._Board(number_of_colors, number_of_dots)
        self._game_started = TrueFuse(False)
        self._win_status = Boolean(None)

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
    def make_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
        """Makes a guess and updates the board."""
        if self._win_status is not None:
            raise NotImplementedError("Cannot make guess after game has ended.")
        if len(self._board) >= self.MAXIMUM_ATTEMPTS:
            raise NotImplementedError("Cannot make guess after maximum attempts reached.")
        self._board.add_guess(guess, feedback)

    def update_win_status(self, win_status: bool) -> None:
        """Updates the win status of the game."""
        if len(self._board) == 0:
            self._win_status = None
        if hasattr(self, 'SECRET_CODE') and self._board.last_guess()[0] == self.SECRET_CODE:
            self._win_status = True
        if self._board.last_guess()[1] == (self.number_of_dots, 0):
            self._win_status = True
        if len(self._board) == self.MAXIMUM_ATTEMPTS:
            self._win_status = False
        else:
            self._win_status = None
        
        return self._win_status

    def find_players(self) -> None:
        """Find suitable player for a game based on the game mode."""
        if self.GAME_MODE == "HvH":
            self.PLAYER1 = HumanCracker(self)
            self.PLAYER2 = HumanSetter(self)
        elif self.GAME_MODE == "HvAI":
            self.PLAYER1 = HumanCracker(self)
            self.PLAYER2 = AISetter(self)
        elif self.GAME_MODE == "AIvH":
            self.PLAYER1 = AICracker(self)
            self.PLAYER2 = HumanSetter(self)
        else:
            self.PLAYER1 = AICracker(self)
            self.PLAYER2 = ExternalSetter(self)

    def player_guessing_logic(self) -> Optional[str]:
        """Call Player 2 to make guess and Player 1 to obtain feedback."""
        while self.win_status is None:
            # Obtain guess or command
            guess = self.PLAYER2.obtain_guess()

            # Process command
            if guess is "q":  # quit
                break
            if guess is "d":  # discard
                break
            if guess is "u":  # undo
                self.PLAYER1.undo()  # Update undo stack for feedback
                self.PLAYER2.undo()  # Update undo stack for guess
                self._board.remove_last()  # Remove the guess and feedback
                continue
            if guess is "r":  # redo
                feedback = self.PLAYER1.redo()  # Retrieve from undo stack
                guess = self.PLAYER2.redo()  # Retrieve from undo stack
                self.make_guess(guess, feedback)  # Add guess and feedback back
                continue
            
            # Get feedback
            feedback = self.PLAYER1.get_feedback(guess)

            # Process command
            if feedback is "q":  # quit
                break
            if feedback is "d":  # discard
                break
            if feedback is "u":  # undo
                continue  # guess haven't been made yet, so skip = undo
            
            # Make Guess
            self.make_guess(guess, feedback)
            self.update_win_status(self._win_status)

    def output_result(self) -> None:
        """Output the result of the game."""
        self.update_win_status(self._win_status)
        if self.win_status is None:
            return
        if self.win_status:
            self.PLAYER2.win_message()
        else:
            self.PLAYER2.lose_message()

    # Game Flow Logic
    def start_game(self) -> Optional[str]:
        """Starts the game."""
        # Check Condition
        if self._game_started:
            raise NotImplementedError("Game has already started.")
        
        # Start Game
        self._game_started = True
        self.find_players()
        self.PLAYER1.set_secret_code()

        command = self.player_guessing_logic()  # Sometimes user quit or discard

        # Post-termination Logic
        self.output_result()
        return command

    def resume_game(self) -> None:
        """Resumes the game."""
        # Check Condition
        if not self._game_started:
            raise NotImplementedError("Game has not started yet.")
        
        command = self.player_guessing_logic()  # Play game and retrieve command
        
        # Post-termination Logc
        self.output_result()
        return command

