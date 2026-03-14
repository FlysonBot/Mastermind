"""Tests for computer.play() — Python-side logic only.

Mocks:
  - ask_game_settings / ask_secret  (setup prompts)
  - MastermindSession               (Java)
  - Feedback                        (Java class — whole object replaced)
  - display                         (Java-backed)
  - console / pause                 (output side-effects)
"""

from unittest.mock import MagicMock, patch


def _fb(black, white):
    return black * 10 + white


def _fake_feedback(return_value=None, side_effect=None):
    fb = MagicMock()
    if side_effect is not None:
        fb.getFeedback.side_effect = side_effect
    else:
        fb.getFeedback.return_value = return_value
    return fb


def _make_session(suggestions):
    session = MagicMock()
    session.suggestGuess.side_effect = suggestions
    return session


class TestComputerPlay:
    def test_solves_on_first_guess(self):
        with (
            patch("mastermind.gamemode.computer.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.computer.ask_secret") as ask_secret,
            patch("mastermind.gamemode.computer.MastermindSession") as SessionClass,
            patch("mastermind.gamemode.computer.Feedback", _fake_feedback(_fb(4, 0))),
            patch("mastermind.gamemode.computer.display", return_value="1234"),
            patch("mastermind.gamemode.computer.console") as console,
            patch("mastermind.gamemode.computer.pause") as pause,
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            SessionClass.return_value = _make_session([7])

            from mastermind.gamemode.computer import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "solved" in printed.lower() or "✓" in printed
            pause.assert_called_once()

    def test_win_message_singular_try(self):
        with (
            patch("mastermind.gamemode.computer.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.computer.ask_secret") as ask_secret,
            patch("mastermind.gamemode.computer.MastermindSession") as SessionClass,
            patch("mastermind.gamemode.computer.Feedback", _fake_feedback(_fb(4, 0))),
            patch("mastermind.gamemode.computer.display", return_value="1234"),
            patch("mastermind.gamemode.computer.console") as console,
            patch("mastermind.gamemode.computer.pause"),
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            SessionClass.return_value = _make_session([7])

            from mastermind.gamemode.computer import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "try" in printed

    def test_win_message_plural_tries(self):
        with (
            patch("mastermind.gamemode.computer.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.computer.ask_secret") as ask_secret,
            patch("mastermind.gamemode.computer.MastermindSession") as SessionClass,
            patch(
                "mastermind.gamemode.computer.Feedback",
                _fake_feedback(side_effect=[_fb(0, 0), _fb(4, 0)]),
            ),
            patch("mastermind.gamemode.computer.display", return_value="1234"),
            patch("mastermind.gamemode.computer.console") as console,
            patch("mastermind.gamemode.computer.pause"),
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            SessionClass.return_value = _make_session([7, 8])

            from mastermind.gamemode.computer import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "tries" in printed

    def test_records_each_non_winning_guess(self):
        with (
            patch("mastermind.gamemode.computer.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.computer.ask_secret") as ask_secret,
            patch("mastermind.gamemode.computer.MastermindSession") as SessionClass,
            patch(
                "mastermind.gamemode.computer.Feedback",
                _fake_feedback(side_effect=[_fb(0, 0), _fb(1, 1), _fb(4, 0)]),
            ),
            patch("mastermind.gamemode.computer.display", return_value="1234"),
            patch("mastermind.gamemode.computer.console"),
            patch("mastermind.gamemode.computer.pause"),
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            session = _make_session([1, 2, 3])
            SessionClass.return_value = session

            from mastermind.gamemode.computer import play

            play()

            # recordGuess called for every guess including the winning one
            assert session.recordGuess.call_count == 3

    def test_out_of_tries_shows_secret(self):
        with (
            patch("mastermind.gamemode.computer.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.computer.ask_secret") as ask_secret,
            patch("mastermind.gamemode.computer.MastermindSession") as SessionClass,
            patch(
                "mastermind.gamemode.computer.Feedback",
                _fake_feedback(side_effect=[_fb(0, 0), _fb(1, 0)]),
            ),
            patch("mastermind.gamemode.computer.display", return_value="5555"),
            patch("mastermind.gamemode.computer.console") as console,
            patch("mastermind.gamemode.computer.pause") as pause,
        ):
            ask_settings.return_value = (6, 4, 2)
            ask_secret.return_value = 0
            SessionClass.return_value = _make_session([1, 2])

            from mastermind.gamemode.computer import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "failed" in printed.lower() or "✗" in printed
            assert "5555" in printed
            pause.assert_called_once()

    def test_each_guess_printed(self):
        with (
            patch("mastermind.gamemode.computer.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.computer.ask_secret") as ask_secret,
            patch("mastermind.gamemode.computer.MastermindSession") as SessionClass,
            patch(
                "mastermind.gamemode.computer.Feedback",
                _fake_feedback(side_effect=[_fb(2, 1), _fb(4, 0)]),
            ),
            patch("mastermind.gamemode.computer.display", return_value="1234"),
            patch("mastermind.gamemode.computer.console") as console,
            patch("mastermind.gamemode.computer.pause"),
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            SessionClass.return_value = _make_session([1, 2])

            from mastermind.gamemode.computer import play

            play()

            printed_lines = [str(c) for c in console.print.call_args_list]
            guess_lines = [l for l in printed_lines if "Guess" in l]
            assert len(guess_lines) == 2
