from abc import ABC, abstractmethod
from getpass import getpass
from random import randint
from typing import Optional, Union

from .utils import FStringTemplate, get_feedback, Stack
from .validation import BaseModel, ValidFeedback, ValidGuess


# Abstract Class for Player Unit
class Player(ABC, BaseModel):
    """A class to represent a player."""

    def __init__(self, game: 'Game') -> None:
        """Initializes the player."""
        self.GAME = game
        self.undo_stack = Stack()  # For undo and redo functionality

    def undo(self) -> None:
        """Update the undo stack so we can redo afterward."""
        if len(self.GAME._board) == 0:
            raise self.GAME._board.EmptyBoardError("Cannot undo from empty board.")
        self.undo_stack.push(self.GAME._board.last_guess())

    def redo(self) -> None:
        """Pop from the undo stack and return the last guess."""
        if len(self.undo_stack) == 0:
            raise IndexError("Cannot undo from empty board.")
        return self.undo_stack.pop()


class CodeSetter(Player):
    """A class to represent a code setter."""

    @abstractmethod
    def set_secret_code(self) -> None:
        """Sets the secret code for the game."""
        pass

    @abstractmethod
    def get_feedback(self, guess: tuple) -> tuple:
        """Obtains feedback for a given guess."""
        pass


class CodeCracker(Player):
    """A class to represent a code cracker."""

    def __init__(self, game: 'Game', win_msg: str, lose_msg: str) -> None:
        """Initializes the code cracker."""
        super().__init__(game)
        self._win_message = FStringTemplate(win_msg)
        self._lose_message = FStringTemplate(lose_msg)

    def win_message(self) -> None:
        """Prints a message when the game is won."""
        print(self._win_message.eval(self.__dict__))

    def lose_message(self) -> None:
        """Prints a message when the game is lost."""
        print(self._lose_message.eval(self.__dict__))

    @abstractmethod
    def obtain_guess(self) -> tuple:
        """Obtains a guess from the player."""
        pass


# Concrete Implementation of Different Players
class HumanSetter(CodeSetter):
    """A class to represent a human code setter."""

    def set_secret_code(self) -> Optional[str]:
        """
        Sets the secret code for the game.
        Return 'd' if player discarded the game. Otherwise doesn't return anything.
        """
        valid_guess = ValidGuess(
            [1] * self.GAME.number_of_dots,
            number_of_dots=self.GAME.number_of_dots,
            number_of_colors=self.GAME.number_of_colors,
        )
        while True:
            secret = getpass("Enter the secret code: ")
            if secret == "?":
                hint = f"""
                Enter a {self.GAME.number_of_dots}-digit number with digit ranging from 1 to {self.GAME.number_of_colors}.
                For example, a 6-digit 4-color code can be 123412, or 1,2,3,4,1,2
                Or, you can enter a command:
                (?) for help
                (d) to discard the game
                """
                print(hint)
                continue
            if secret == "d":
                print("Game discarded.")
                return "d"

            try:
                valid_guess.value = valid_guess.validate(secret)
            except ValueError as e:
                print(e)
                print("To get more help, enter '?'")
            else:  # Confirm password
                confirm = getpass("Confirm the secret code: ")
                if confirm != secret:
                    print("Code does not match. Try again.")
                    continue
                self.SECRET_CODE = valid_guess
                return

    def get_feedback(self, guess: tuple) -> tuple:
        """Obtains feedback for a given guess."""
        if not hasattr(self, "SECRET_CODE"):
            raise NotImplementedError("Secret code not set yet.")
        return get_feedback(guess, self.SECRET_CODE, self.GAME.number_of_colors)


class AISetter(CodeSetter):
    """A class to represent an AI code setter."""

    def set_secret_code(self) -> None:
        """Sets the secret code for the game."""
        # Generate random code
        number_of_colors = self.GAME.number_of_colors
        number_of_dots = self.GAME.number_of_dots
        self.SECRET_CODE = tuple(
            randint(1, number_of_colors) for _ in range(number_of_dots)
        )

    def get_feedback(self, guess: tuple) -> tuple:
        """Obtains feedback for a given guess."""
        if not hasattr(self, "SECRET_CODE"):
            raise NotImplementedError("Secret code not set yet.")
        return get_feedback(guess, self.SECRET_CODE, self.GAME.number_of_colors)


class ExternalSetter(CodeSetter):
    """A class to represent an external code setter."""

    def set_secret_code(self) -> None:
        """Sets the secret code for the game."""
        pass  # There is no code available for external game, skip it

    def get_feedback(self, guess: tuple) -> Union[tuple, str]:
        """
        Obtains external feedback from the user.
        Could return the feedback as tuple or command (d,q,u) as string.
        """
        valid_feedback = ValidFeedback((0, 0), number_of_dots=self.GAME.number_of_dots)
        while True:
            feedback = input("Enter the feedback: ")
            if feedback == "?":
                hint = f"""
                Enter a 2 digit number (optionally separated by comma) between 0 and {self.GAME.number_of_dots}.
                The first digit represents the number of black pegs, the second represents the number of white pegs.
                For example: 01 or 0,1 -> (0, 1) -> 0 black pegs, 1 white peg.
                Or, you can enter a command:
                (?) for help
                (d) to discard the game
                (q) to save and quit
                (u) to undo
                """
                print(hint)
                continue
            if feedback == "d":
                print("Game discarded.")
                return "d"
            if feedback == "q":  # quit
                print("Game saved.")
                return "q"
            if feedback == "u":  # undo
                return "u"

            try:
                valid_feedback.value = valid_feedback.validate(feedback)
                return valid_feedback.value
            except ValueError as e:
                print(e)
                print("To get more help, enter '?'")


class HumanCracker(CodeCracker):
    """A class to represent a human code cracker."""

    def __init__(self, game: 'Game') -> None:
        """Initializes the human code cracker."""
        win_message = "Congratulations! You won in {step} steps!"
        lose_message = "Sorry, you lost. The secret code was {secret_code}."
        super().__init__(game, win_message, lose_message)

    def obtain_guess(self) -> Union[tuple, str]:
        """
        Obtains a guess from the player.
        Could return the guess as tuple or command (d,q,u,r) as string.
        """
        valid_guess = ValidGuess(
            [1] * self.GAME.number_of_dots,
            number_of_dots=self.GAME.number_of_dots,
            number_of_colors=self.GAME.number_of_colors,
        )
        while True:
            guess = input("Enter your guess: ")
            if guess == "?":
                hint = f"""
                Enter a {self.GAME.number_of_dots}-digit number with digit ranging from 1 to {self.GAME.number_of_colors}.
                For example, a 6-digit 4-color code can be 123412, or 1,2,3,4,1,2
                Or, you can enter a command:
                (?) for help
                (d) to discard the game
                (q) to save and quit
                (u) to undo
                (r) to redo
                """
                print(hint)
                continue
            if guess == "d":
                print("Game discarded.")
                return "d"
            if guess == "q":  # quit
                print("Game saved.")
                return "q"
            if guess == "u":  # undo
                return "u"
            if guess == "r":  # redo
                return "r"

            try:
                valid_guess.value = valid_guess.validate(guess)
                return valid_guess.value
            except ValueError as e:
                print(e)
                print("To get more help, enter '?'")


class AICracker(CodeCracker):
    """A class to represent an AI code cracker."""

    pass  # TODO: Implement solver logic.
