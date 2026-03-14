"""Tests for assisted.play() — Python-side logic only.

Mocks:
  - ask_game_settings               (setup prompt)
  - MastermindSession               (Java)
  - Prompt.ask / IntPrompt.ask      (user input)
  - parse_code                      (Java-backed)
  - display                         (Java-backed)
  - console.print / pause           (output side effects)

jpype.JException is replaced with a plain exception subclass so we can
raise it from mocks without a running JVM.
"""

from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fb(black, white):
    return black * 10 + white


class _FakeJException(Exception):
    """Stand-in for jpype.JException in tests."""


def _make_session(suggestions, solution_sizes=None):
    """
    suggestions: list of ints returned by suggestGuess (in order).
    solution_sizes: list of ints returned by getSolutionSpaceSize (in order).
                    Defaults to [100, 50, 10, ...] (shrinking).
    """
    session = MagicMock()
    session.suggestGuess.side_effect = [int(s) for s in suggestions]
    if solution_sizes is None:
        solution_sizes = list(range(100, 0, -10))
    session.getSolutionSpaceSize.side_effect = solution_sizes
    return session


BASE_PATCHES = dict(
    ask_settings="mastermind.gamemode.assisted.ask_game_settings",
    SessionClass="mastermind.gamemode.assisted.MastermindSession",
    prompt="mastermind.gamemode.assisted.Prompt.ask",
    int_prompt="mastermind.gamemode.assisted.IntPrompt.ask",
    parse_code="mastermind.gamemode.assisted.parse_code",
    display="mastermind.gamemode.assisted.display",
    console="mastermind.gamemode.assisted.console",
    pause="mastermind.gamemode.assisted.pause",
    jpype_exc="mastermind.gamemode.assisted.jpype.JException",
)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAssistedPlay:
    def test_win_using_suggestion(self):
        """Accept the suggested guess and receive a perfect score → win."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]) as pause,
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            SessionClass.return_value = _make_session([7])
            # Prompt returns suggestion string → accepted; then feedback = "4b0w"
            prompt.side_effect = ["1234", "4b0w"]

            from mastermind.gamemode.assisted import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Perfect" in printed or "✓" in printed
            pause.assert_called_once()

    def test_win_using_custom_guess(self):
        """Enter a different code (not suggestion) and win."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]) as parse_code,
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]) as pause,
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            SessionClass.return_value = _make_session([7])
            # User enters "5678" (custom), then feedback = perfect
            prompt.side_effect = ["5678", "4b0w"]
            parse_code.return_value = 99  # valid custom guess

            from mastermind.gamemode.assisted import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Perfect" in printed or "✓" in printed

    def test_invalid_guess_retried(self):
        """Invalid guess input loops until a valid one is entered."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]) as parse_code,
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            SessionClass.return_value = _make_session([7])
            # "bad" is not the suggestion, parse_code returns None for it
            prompt.side_effect = ["bad", "1234", "4b0w"]
            parse_code.side_effect = [None, 42]

            from mastermind.gamemode.assisted import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Invalid" in printed

    def test_invalid_feedback_retried(self):
        """Invalid feedback loops until a valid one is entered."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = _make_session([7], solution_sizes=[100])
            SessionClass.return_value = session
            # Guess accepted (suggestion), then bad feedback, then good feedback = win
            prompt.side_effect = ["1234", "xyz", "4b0w"]

            from mastermind.gamemode.assisted import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Invalid" in printed

    def test_u_at_guess_prompt_on_first_turn_does_nothing(self):
        """'u' on turn 1 at guess prompt prints a warning and re-prompts."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            SessionClass.return_value = _make_session([7])
            # 'u' on first turn, then accept suggestion, then win
            prompt.side_effect = ["u", "1234", "4b0w"]

            from mastermind.gamemode.assisted import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Nothing to undo" in printed

    def test_u_at_guess_prompt_undoes_previous_turn(self):
        """'u' on turn 2 calls session.undo(1) and goes back to turn 1."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]),
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = _make_session([7, 7], solution_sizes=[100, 50])
            SessionClass.return_value = session
            # Turn 1: accept suggestion, non-winning feedback
            # Turn 2 guess: 'u' → undo
            # Turn 1 again: accept suggestion, win
            prompt.side_effect = ["1234", "1b0w", "u", "1234", "4b0w"]

            from mastermind.gamemode.assisted import play

            play()

            session.undo.assert_called_once_with(1)

    def test_u_at_feedback_prompt_rerequests_guess(self):
        """'u' at feedback prompt re-asks the guess for the same turn (no session undo)."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = _make_session([7], solution_sizes=[100])
            SessionClass.return_value = session
            # Guess accepted, feedback 'u' → re-ask guess, then accept again and win
            prompt.side_effect = ["1234", "u", "1234", "4b0w"]

            from mastermind.gamemode.assisted import play

            play()

            # session.undo should NOT be called (u at feedback, not guess)
            session.undo.assert_not_called()
            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Re-enter" in printed

    def test_out_of_turns(self):
        """Exhaust max_tries without a win → out-of-turns message."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]) as pause,
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 2)
            session = _make_session([7, 8], solution_sizes=[100, 50])
            SessionClass.return_value = session
            # 2 turns, each: accept suggestion + non-winning feedback
            prompt.side_effect = ["1234", "1b0w", "1234", "0b1w"]

            from mastermind.gamemode.assisted import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Out of turns" in printed or "✗" in printed
            pause.assert_called_once()

    def test_suggestion_cached_on_undo(self):
        """After undo, the cached suggestion for that turn is re-used (suggestGuess not called again)."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]),
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = _make_session([7, 8], solution_sizes=[100, 50])
            SessionClass.return_value = session
            # Turn 1: accept + non-winning; Turn 2: undo; Turn 1 again: accept + win
            prompt.side_effect = ["1234", "1b0w", "u", "1234", "4b0w"]

            from mastermind.gamemode.assisted import play

            play()

            # suggestGuess called only once for turn 1 (cached on re-visit)
            assert session.suggestGuess.call_count == 2  # turn1 + turn2 before undo

    def test_remaining_percentage_printed(self):
        """After a non-winning turn, the eliminated % and remaining count are printed."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            # c**d = 6**4 = 1296, after guess: 648 remain → 50% eliminated
            session = _make_session([7, 8], solution_sizes=[648, 1])
            SessionClass.return_value = session
            prompt.side_effect = ["1234", "1b0w", "1234", "4b0w"]

            from mastermind.gamemode.assisted import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "eliminated" in printed
            assert "remaining" in printed

    def test_inconsistent_feedback_offers_undo(self):
        """When session raises 'No valid secrets remain', user is offered undo."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]) as int_prompt,
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]) as pause,
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = MagicMock()
            session.suggestGuess.side_effect = [7, 8]
            session.getSolutionSpaceSize.return_value = 100
            # First recordGuess raises; second (after undo) is fine and leads to win
            exc = _FakeJException("No valid secrets remain")
            session.recordGuess.side_effect = [exc, None]
            SessionClass.return_value = session

            # Turn 1: accept suggestion, bad feedback (raises) → undo 1 → turn 1 again → win
            prompt.side_effect = ["1234", "1b0w", "y", "1234", "4b0w"]
            int_prompt.return_value = 1

            from mastermind.gamemode.assisted import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "inconsistent" in printed.lower() or "No valid" in printed

    def test_inconsistent_feedback_user_declines_undo_exits(self):
        """When inconsistency is detected and user says 'n', game exits."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]),
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]),
            patch(BASE_PATCHES["pause"]) as pause,
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = MagicMock()
            session.suggestGuess.return_value = 7
            exc = _FakeJException("No valid secrets remain")
            session.recordGuess.side_effect = exc
            SessionClass.return_value = session

            # Turn 1: accept suggestion, bad feedback (raises) → user says "n" → exit
            prompt.side_effect = ["1234", "1b0w", "n"]

            from mastermind.gamemode.assisted import play

            play()

            pause.assert_called_once()

    def test_inconsistent_undo_1_resumes_from_turn_1(self):
        """After inconsistency on turn 1, undo 1 → session.undo(1) called, resumes from turn 1."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]) as int_prompt,
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]),
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = MagicMock()
            session.suggestGuess.side_effect = [7, 8]
            session.getSolutionSpaceSize.return_value = 100
            exc = _FakeJException("No valid secrets remain")
            session.recordGuess.side_effect = [exc, None]
            SessionClass.return_value = session

            # Turn 1: accept, bad feedback → exception → undo 1 → turn 1 again → win
            prompt.side_effect = ["1234", "1b0w", "y", "1234", "4b0w"]
            int_prompt.return_value = 1

            from mastermind.gamemode.assisted import play

            play()

            session.undo.assert_called_once_with(1)

    def test_inconsistent_undo_2_resumes_from_correct_turn(self):
        """After inconsistency on turn 2, undo 2 → session.undo(2), resumes from turn 1."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]) as int_prompt,
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]),
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = MagicMock()
            # Turn 1 succeeds, turn 2 raises, then turn 1 again wins
            session.suggestGuess.side_effect = [7, 8, 9]
            session.getSolutionSpaceSize.side_effect = [50, 50]
            exc = _FakeJException("No valid secrets remain")
            session.recordGuess.side_effect = [None, exc, None]
            SessionClass.return_value = session

            # Turn 1: accept + good feedback
            # Turn 2: accept + bad feedback → exception → undo 2 → turn 1 again → win
            prompt.side_effect = ["1234", "1b0w", "1234", "0b1w", "y", "1234", "4b0w"]
            int_prompt.return_value = 2

            from mastermind.gamemode.assisted import play

            play()

            session.undo.assert_called_once_with(2)

    def test_inconsistent_invalid_undo_count_reprompted(self):
        """Out-of-range undo count is rejected and re-prompted."""
        with (
            patch(BASE_PATCHES["ask_settings"]) as ask_settings,
            patch(BASE_PATCHES["SessionClass"]) as SessionClass,
            patch(BASE_PATCHES["prompt"]) as prompt,
            patch(BASE_PATCHES["int_prompt"]) as int_prompt,
            patch(BASE_PATCHES["parse_code"]),
            patch(BASE_PATCHES["display"], return_value="1234"),
            patch(BASE_PATCHES["console"]) as console,
            patch(BASE_PATCHES["pause"]),
            patch(BASE_PATCHES["jpype_exc"], _FakeJException),
        ):
            ask_settings.return_value = (6, 4, 10)
            session = MagicMock()
            session.suggestGuess.side_effect = [7, 8]
            session.getSolutionSpaceSize.return_value = 100
            exc = _FakeJException("No valid secrets remain")
            session.recordGuess.side_effect = [exc, None]
            SessionClass.return_value = session

            # Turn 1: accept, bad feedback → exception → undo prompt: 0 (invalid), then 1 (valid) → win
            prompt.side_effect = ["1234", "1b0w", "y", "1234", "4b0w"]
            int_prompt.side_effect = [0, 1]  # first out of range, second valid

            from mastermind.gamemode.assisted import play

            play()

            # IntPrompt asked twice (once invalid, once valid)
            assert int_prompt.call_count == 2
            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Must be between" in printed
