from abc import ABC, abstractmethod

from src.game import Game
from src.utils import FStringTemplate, Stack
from src.validation import BaseModel


class Player(ABC, BaseModel):
    def __init__(self, game: Game) -> None:  # type: ignore
        self.GAME = game
        self.undo_stack = Stack()  # For undo and redo functionality

    @abstractmethod
    def undo(self, item: tuple) -> None:
        if len(self.GAME._board) == 0:
            raise self.GAME._board.EmptyBoardError("Cannot undo from empty board.")

        # Item can be guess or feedback, varies by player type
        self.undo_stack.push(item)

    def redo(self) -> None:
        if len(self.undo_stack) == 0:
            raise IndexError("Cannot undo from empty board.")
        return self.undo_stack.pop()

    def clear_undo(self) -> None:
        self.undo_stack.clear()


class CodeSetter(Player, ABC):
    @abstractmethod
    def set_secret_code(self) -> None:
        pass

    @abstractmethod
    def get_feedback(self, guess: tuple) -> tuple:
        pass

    def undo(self) -> None:
        super().undo(self.GAME._board.last_feedback())


class CodeCracker(Player, ABC):
    def __init__(self, game: "Game", win_msg: str, lose_msg: str) -> None:  # type: ignore
        super().__init__(game)
        self._win_message = FStringTemplate(win_msg)
        self._lose_message = FStringTemplate(lose_msg)

    def win_message(self) -> None:
        print(self._win_message.eval(step=len(self.GAME)))

    def lose_message(self) -> None:
        print(self._lose_message.eval(step=len(self.GAME)))

    @abstractmethod
    def obtain_guess(self) -> tuple:
        pass

    def undo(self) -> None:
        super().undo(self.GAME._board.last_guess())
