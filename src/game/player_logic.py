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
        """Determines and assigns players based on the game mode."""
        if self.GAME_MODE == "HvH":
            self.PLAYER_CRACKER = HumanCodeCracker(self)
            self.PLAYER_SETTER = HumanCodeSetter(self)

        elif self.GAME_MODE == "HvAI":
            self.PLAYER_CRACKER = HumanCodeCracker(self)
            self.PLAYER_SETTER = AICodeSetter(self)

        elif self.GAME_MODE == "AIvH":
            self.PLAYER_CRACKER = AICodeCracker(self)
            self.PLAYER_SETTER = HumanCodeSetter(self)

        else:
            self.PLAYER_CRACKER = AICodeCracker(self)
            self.PLAYER_SETTER = ExternalCodeSetter(self)

    def process_player_guessing(self) -> Optional[str]:
        """Handle the logic for player guessing."""
        while self.game_state.win_status is None:
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
                self.game_state._board.remove_last()
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
            self.game_state.check_and_update_win_status()

    def submit_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
        """
        Submits a player's guess and updates the game board with the corresponding feedback.

        This function checks if the game is still ongoing and if the maximum number of
        attempts has not been reached before adding the guess and feedback to the board.
        It also clears any undo actions for both the guesser and the setter.
        """
        if self._win_status is not None:
            raise NotImplementedError("Cannot make guess after game has ended.")

        self.PLAYER_CRACKER.clear_undo()
        self.PLAYER_SETTER.clear_undo()
        self._board.add_guess(guess, feedback)
