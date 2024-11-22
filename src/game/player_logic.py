from typing import Optional, Tuple

from src.game.game_state import GameState
from src.players import (
    AICodeCracker,
    AICodeSetter,
    ExternalCodeSetter,
    HumanCodeCracker,
    HumanCodeSetter,
)


class PlayerLogic:
    def __init__(self, game: GameState) -> None:
        self.game_state = game

    @property
    def GAME_MODE(self) -> str:
        return self.game_state.GAME_MODE

    def initialize_players(self) -> None:
        game_mode_mapping = {
            "HvH": (HumanCodeCracker, HumanCodeSetter),
            "HvAI": (HumanCodeCracker, AICodeSetter),
            "AIvH": (AICodeCracker, HumanCodeSetter),
            "AIvAI": (AICodeCracker, ExternalCodeSetter),
        }

        if self.GAME_MODE in game_mode_mapping:
            self.PLAYER_CRACKER, self.PLAYER_SETTER = (
                cls(self) for cls in game_mode_mapping[self.GAME_MODE]
            )

    def process_player_guessing(self) -> Optional[str]:
        while self.game_state.win_status is None:
            guess = self.PLAYER_CRACKER.obtain_guess()

            # Process commands
            if guess in {"q", "d"}:  # quit or discard
                return guess
            if guess == "u":  # undo
                self._undo_logic()
                continue
            if guess == "r":  # redo
                self._redo_logic()
                continue

            feedback = self.PLAYER_SETTER.get_feedback(guess)

            # Process command
            if feedback in {"q", "d"}:  # quit or discard
                break
            if feedback == "u":  # undo
                continue  # since guess haven't been submitted, skip = undo

            self.submit_guess(guess, feedback)
            self.game_state.check_and_update_win_status()

    def _undo_logic(self) -> None:
        self.PLAYER_CRACKER.undo()
        self.PLAYER_SETTER.undo()
        self.game_state._board.remove_last()

    def _redo_logic(self) -> None:
        guess = self.PLAYER_CRACKER.redo()
        feedback = self.PLAYER_SETTER.redo()
        self.submit_guess(guess, feedback)

    def submit_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
        if self._win_status is not None:
            raise NotImplementedError("Cannot make guess after game has ended.")

        self.PLAYER_CRACKER.clear_undo()
        self.PLAYER_SETTER.clear_undo()
        self._board.add_guess(guess, feedback)
