from .validation import BaseModel
from collections import deque
from typing import Any, Optional


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
        self.number_of_colors = number_of_colors
        self.number_of_dots = number_of_dots
        self.guesses = Stack()
        self.feedbacks = Stack()
        self.number_of_guesses_made = 0
    
    
    # Accessors
    def __len__(self) -> int:
        """
        Returns the number of guesses made.
        """
        return self.number_of_guesses_made
    
    def __getitem__(self, index: int) -> tuple:
        """
        Returns the guess and feedback at the given index.
        Index is counted from the top, i.e. 0 represent the last.
        """
        return self.guesses[index], self.feedbacks[index]
    
    def last_guess(self) -> tuple:
        """
        Returns the last guess and its feedback.
        """
        # Check if board is empty
        if self.number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to return.")
        
        # Return
        return self.guesses.top(), self.feedbacks.top()


    # Mutators
    def add_guess(self, guess: tuple, feedback: tuple) -> None:
        """
        Adds a guess and its feedback to the board.
        """
        # Validate input
        ValidGuess(guess, number_of_dots=self.number_of_dots, number_of_colors=self.number_of_colors)
        ValidFeedback(feedback, number_of_dots=self.number_of_dots)

        # Make changes
        self.guesses.push(guess)
        self.feedbacks.push(feedback)
        self.number_of_guesses_made += 1
    
    def remove_last_guess(self) -> tuple:
        """
        Undoes the last guess and its feedback.
        """
        # Check if board is empty
        if self.number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to remove.")
        
        # Make changes
        guess = self.guesses.pop()
        feedback = self.feedbacks.pop()
        self.number_of_guesses_made -= 1

        return guess, feedback
        
    def clear_board(self) -> None:
        """
        Clears the board.
        """
        self.guesses.clear_stack()
        self.feedbacks.clear_stack()
        self.number_of_guesses_made = 0
        