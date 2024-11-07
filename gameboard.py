# gameboard.py
from .validation import BaseModel
from .utils import get_feedback
from collections import deque
from typing import Any, Optional, Tuple
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
    def make_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
        """
        Makes a guess and updates the board.
        """
        # Check condition
        if self._win_status is not None:
            raise NotImplementedError("Cannot make guess after game has ended.")
        if len(self._board) >= self.MAXIMUM_ATTEMPTS:
            raise NotImplementedError("Cannot make guess after maximum attempts reached.")
                
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
    
    # Game Control Methods
    def find_players(self) -> None:
        """
        Find suitable player for a game based on the game mode.
        """
        if self.GAME_MODE == "HvH":  # Human against Human
            self.PLAYER1 = HumanCracker(self)
            self.PLAYER2 = HumanSetter(self)
        elif self.GAME_MODE == "HvAI":  # Human against AI
            self.PLAYER1 = HumanCracker(self)
            self.PLAYER2 = AISetter(self)
        elif self.GAME_MODE == "AIvH":  # AI against Human
            self.PLAYER1 = AICracker(self)
            self.PLAYER2 = HumanSetter(self)
        else:  # GAME_MODE = "AIvAI", solving external game
            self.PLAYER1 = AICracker(self)
            self.PLAYER2 = ExternalSetter(self)

    def player_guessing_logic(self) -> None:
        """
        Call Player 2 to make guess and Player 1 to obtain feedback.
        """
        while self.win_status is None :  # While game is continuing
            guess = self.PLAYER2.obtain_guess()  # Obtain guess
            if guess is None:  # Player 2 quit
                break  # exit the loop
            feedback = self.PLAYER1.get_feedback(guess)  # Obtain feedback
            self.make_guess(guess, feedback)  # Make guess
            self.update_win_status(self._win_status)  # Update win status

    def output_result(self) -> None:
        """
        Output the result of the game.
        """
        self.update_win_status(self._win_status)
        if self.win_status is None:
            return  # game paused and exit
        if self.win_status:
            self.PLAYER2.win_message()
        else:
            self.PLAYER2.lose_message()

    def start_game(self) -> None:
        """
        Starts the game.
        """
        # Check condition
        if self._game_started:
            raise NotImplementedError("Game has already started.")
        self._game_started = True

        # Player Logic
        self.find_players()  # Find suitable player for the game
        self.PLAYER1.set_secret_code()
        self.player_guessing_logic()  # Player guessing logic

        # Game Terminated
        self.output_result()  # Output the result of the game

    def resume_game(self) -> None:
        """
        Resumes the game.
        """
        # Check condition
        if not self._game_started:
            raise NotImplementedError("Game has not started yet.")
        
        # Player Logic
        self.player_guessing_logic()  # Player guessing logic

        # Game Terminated
        self.output_result()  # Output the result of the game


