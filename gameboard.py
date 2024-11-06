from .validation import BaseModel
from .utils import get_feedback
from collections import deque
from typing import Any, Optional
from random import randint


class Stack:
    """
    An implementation of a stack data structure using deque.
    """
    def __init__(self, data: Optional[list] = None) -> None:
        """
        Initializes the stack.
        """
        self._stack = deque(data) if data else deque()

    def push(self, item: Any) -> None:
        """
        Adds an item to the top of the stack.
        """
        self._stack.append(item)

    def pop(self) -> Any:
        """
        Removes and returns the top item from the stack.
        """
        if self.is_empty():
            raise IndexError("No items to pop.")
        return self._stack.pop()

    def top(self) -> Any:
        """
        Returns the top item from the stack without removing it.
        """
        if self.is_empty():
            raise IndexError("No items to top.")
        return self._stack[-1]

    def is_empty(self) -> bool:
        """
        Returns True if the stack is empty, False otherwise.
        """
        return len(self._stack) == 0

    def __len__(self) -> int:
        """
        Returns the number of items in the stack.
        """
        return len(self._stack)

    def __getitem__(self, index: int) -> Any:
        """
        Returns the item at the given index counted from the top.
        """
        if index < 0 or index >= len(self._stack):
            raise IndexError("Index out of range.")
        return self._stack[-(index + 1)]

    def clear_stack(self) -> None:
        """
        Clears the stack.
        """
        self._stack.clear()

    @property
    def stack(self) -> list:
        """
        Returns the stack as a list. DO NOT EDIT THIS LIST.
        """
        return list(self._stack)

    def __iter__(self):
        """Return an iterator for the stack."""
        return iter(self._stack)


class Game(BaseModel):
    """
    A class to represent a Mastermind game.
    """
    # Board subclass
    class _Board(BaseModel):
        """
        A class to represent a Mastermind board. The board contain all
        the guesses made by a player and the feedback for each guess.
        """
        class EmptyBoardError(Exception):
            """Custom exception for empty board."""
            pass

        def __init__(self, number_of_colors: int, number_of_dots: int) -> None:
            """
            Initializes the board.
            """
            self.NUMBER_OF_COLORS = number_of_colors
            self.NUMBER_OF_DOTS = number_of_dots
            self._number_of_guesses_made = 0
            self._guesses = Constant(Stack())  # avoid modification to the reference
            self._feedbacks = Constant(Stack())  # stack is still modifiable
        
        
        # Accessors
        def __len__(self) -> int:
            """
            Returns the number of guesses made.
            """
            return self._number_of_guesses_made
        
        def __getitem__(self, index: int) -> tuple:
            """
            Returns the guess and feedback at the given index.
            Index is counted from the top, i.e. 0 represent the last.
            """
            return self._guesses[index], self._feedbacks[index]
        
        def last_guess(self) -> tuple:
            """
            Returns the last guess and its feedback.
            """
            # Check if board is empty
            if self._number_of_guesses_made == 0:
                raise self.EmptyBoardError("No guesses to return.")
            
            # Return
            return self._guesses.top(), self._feedbacks.top()


        # Mutators
        def add_guess(self, guess: tuple, feedback: tuple) -> None:
            """
            Adds a guess and its feedback to the board.
            """
            # Validate input
            ValidGuess(guess, number_of_dots=self.NUMBER_OF_DOTS, number_of_colors=self.NUMBER_OF_COLORS)
            ValidFeedback(feedback, number_of_dots=self.NUMBER_OF_DOTS)

            # Make changes
            self._guesses.push(guess)
            self._feedbacks.push(feedback)
            self._number_of_guesses_made += 1
        
        def remove_last_guess(self) -> tuple:
            """
            Undoes the last guess and its feedback.
            """
            # Check if board is empty
            if self._number_of_guesses_made == 0:
                raise self.EmptyBoardError("No guesses to remove.")
            
            # Make changes
            guess = self._guesses.pop()
            feedback = self._feedbacks.pop()
            self._number_of_guesses_made -= 1

            return guess, feedback
            
        def clear_board(self) -> None:
            """
            Clears the board.
            """
            self._guesses.clear_stack()
            self._feedbacks.clear_stack()
            self._number_of_guesses_made = 0

    # Initialization
    def __init__(self, number_of_colors: int, number_of_dots: int,
                 maximum_attempts: int, game_mode: str) -> None:
        """
        Initializes the game.
        """
        self.MAXIMUM_ATTEMPTS = maximum_attempts
        self.GAME_MODE = game_mode
        self._board = self._Board(number_of_colors, number_of_dots)
        self._game_started = TrueFuse(False)
        self._win_status = Boolean(None)  # None = game still continuing
    
    
    # Accessor
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
    def set_secret_code(self, secret_code: tuple) -> None:
        """
        Sets the secret code for the game.
        """
        if self._game_started:
            raise NotImplementedError("Cannot set secret code after game has started.")
        
        ValidGuess(secret_code, number_of_dots=self.number_of_dots,
                   number_of_colors=self.number_of_colors)  # Validate
        
        self.SECRET_CODE = secret_code  # Set code and lock it as constant
    
    def set_random_secret_code(self) -> None:
        """
        Sets a random secret code for the game.
        """
        if self._game_started:
            raise NotImplementedError("Cannot set secret code after game has started.")
        
        self.SECRET_CODE = tuple(randint(1, self.number_of_colors) for _ in range(self.number_of_dots))
    
    def make_guess(self, guess: tuple, feedback: Optional[tuple] = None) -> None:
        """
        Makes a guess and updates the board.
        """
        if self._win_status is not None:
            raise NotImplementedError("Cannot make guess after game has ended.")
        if len(self._board) >= self.MAXIMUM_ATTEMPTS:
            raise NotImplementedError("Cannot make guess after maximum attempts reached.")
        if self.GAME_MODE == 'HvAI' and not hasattr(self, 'SECRET_CODE'):
            raise NotImplementedError("Cannot make guess before secret code is set when playing against AI.")
        
        # Calculate feedback if not given
        if feedback is None:
            feedback = get_feedback(guess)
        
        # Add guess and feedback to board
        self._board.add_guess(guess, feedback)  # User input is validated by board
    
    def update_win_status(self, win_status: bool) -> None:
        """
        Updates the win status of the game.
        """
        # No guess made yet, game haven't started
        if len(self._board) == 0:
            self._win_status = None  # None represent continuation of game
        
        # Secret code is set and match with the last guess
        if hasattr(self, 'SECRET_CODE') and self._board.last_guess()[0] == self.SECRET_CODE:
            self._win_status = True
        
        # Last feedback indicates a winning game
        if self._board.last_guess()[1] == (self.number_of_dots, 0):
            self._win_status = True
        
        # Otherwise game is either continuing or had lost
        if len(self._board) == self.MAXIMUM_ATTEMPTS:  # maximum attempt reached
            self._win_status = False  # Lost

        else:  # Otherwise game must be continuing
            self._win_status = None
        
        return self._win_status
    
    # Start the game
    def start_game(self) -> None:
        """
        Starts the game.
        """
        # Check condition
        if self._game_started:
            raise NotImplementedError("Game has already started.")
        self._game_started = True

        # Find suitable player
        if self.GAME_MODE == "HvH":  # Human against Human
            self.PLAYER1 = HumanCracker()
            self.PLAYER2 = HumanSetter()
        elif self.GAME_MODE == "HvAI":  # Human against AI
            self.PLAYER1 = HumanCracker()
            self.PLAYER2 = AISetter()
        elif self.GAME_MODE == "AIvH":  # AI against Human
            self.PLAYER1 = AICracker()
            self.PLAYER2 = HumanSetter()
        else:  # GAME_MODE = "AIvAI", solving external game
            self.PLAYER1 = AICracker()
            self.PLAYER2 = ExternalSetter()
        
        # Player Logic
        pass  # TODO: implement player logic

        # Output Result
        self.update_win_status(self._win_status)
        if self.win_status is None:
            return  # game paused and exit
        if self.win_status:
            self.PLAYER1.win_message()
        else:
            self.PLAYER1.lose_message()

