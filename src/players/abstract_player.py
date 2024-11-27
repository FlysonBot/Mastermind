from abc import ABC, abstractmethod

from src.utils import FStringTemplate, Stack


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
    def __init__(self, player_logic: "PlayerLogic", win_msg: str, lose_msg: str) -> None:  # type: ignore  # noqa: F821
        super().__init__(player_logic)
        self._win_message = FStringTemplate(win_msg)
        self._lose_message = FStringTemplate(lose_msg)

    def win_message(self) -> None:
        print(self._win_message.eval(step=len(self.game_state)))

    def lose_message(self) -> None:
        print(self._lose_message.eval(step=len(self.game_state)))

    @abstractmethod
    def obtain_guess(self) -> tuple:
        pass

    def undo(self) -> None:
        super().undo(self.game_state._board.last_guess())
