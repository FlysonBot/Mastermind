from abc import ABC, abstractmethod

from mastermind.utils import Stack


class Player(ABC):
    def __init__(self, player_logic: "PlayerLogic") -> None:  # type: ignore  # noqa: F821
        self.game_state = player_logic.game_state
        self.undo_stack = Stack()  # For undo and redo functionality

    @abstractmethod
    def undo(self, item: tuple) -> None:
        if len(self.game_state._board) == 0:
            raise self.game_state._board.EmptyBoardError(
                "Cannot undo from empty board."
            )

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
        super().undo(self.game_state._board.last_feedback())


class CodeCracker(Player, ABC):
    @property
    @abstractmethod
    def _WIN_MESSAGE(self) -> str:
        pass

    @property
    @abstractmethod
    def _LOSE_MESSAGE(self) -> str:
        pass

    def win_message(self) -> None:
        print(self._WIN_MESSAGE.format(step=len(self.game_state)))

    def lose_message(self) -> None:
        print(self._LOSE_MESSAGE.format(step=len(self.game_state)))

    @abstractmethod
    def obtain_guess(self) -> tuple:
        pass

    def undo(self) -> None:
        super().undo(self.game_state._board.last_guess())
