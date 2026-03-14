"""Tests for human.play() — Python-side logic only.

Mocks:
  - ask_game_settings / ask_secret  (setup prompts)
  - Prompt.ask                      (guess input)
  - Feedback                        (Java class — whole object replaced)
  - parse_code                      (Java-backed, tested separately)
  - display                         (Java-backed, tested separately)
  - console / pause                 (output side-effects)
"""

from unittest.mock import MagicMock, patch


def _fb(black, white):
    return black * 10 + white


def _fake_feedback(return_value=None, side_effect=None):
    """Return a mock that replaces the Feedback Java class in the module namespace."""
    fb = MagicMock()
    if side_effect is not None:
        fb.getFeedback.side_effect = side_effect
    else:
        fb.getFeedback.return_value = return_value
    return fb


class TestHumanPlay:
    def test_win_on_first_guess(self):
        with (
            patch("mastermind.gamemode.human.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.human.ask_secret") as ask_secret,
            patch("mastermind.gamemode.human.Prompt.ask") as prompt,
            patch("mastermind.gamemode.human.Feedback", _fake_feedback(_fb(4, 0))),
            patch("mastermind.gamemode.human.parse_code", return_value=42),
            patch("mastermind.gamemode.human.display", return_value="1234"),
            patch("mastermind.gamemode.human.console") as console,
            patch("mastermind.gamemode.human.pause") as pause,
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            prompt.return_value = "1234"

            from mastermind.gamemode.human import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Congratulations" in printed or "✓" in printed
            pause.assert_called_once()

    def test_win_message_uses_singular_try(self):
        with (
            patch("mastermind.gamemode.human.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.human.ask_secret") as ask_secret,
            patch("mastermind.gamemode.human.Prompt.ask") as prompt,
            patch("mastermind.gamemode.human.Feedback", _fake_feedback(_fb(4, 0))),
            patch("mastermind.gamemode.human.parse_code", return_value=42),
            patch("mastermind.gamemode.human.display", return_value="1234"),
            patch("mastermind.gamemode.human.console") as console,
            patch("mastermind.gamemode.human.pause"),
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            prompt.return_value = "1234"

            from mastermind.gamemode.human import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "try" in printed  # singular: "1 try"

    def test_win_message_uses_plural_tries(self):
        with (
            patch("mastermind.gamemode.human.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.human.ask_secret") as ask_secret,
            patch("mastermind.gamemode.human.Prompt.ask") as prompt,
            patch(
                "mastermind.gamemode.human.Feedback",
                _fake_feedback(side_effect=[_fb(0, 0), _fb(4, 0)]),
            ),
            patch("mastermind.gamemode.human.parse_code", return_value=42),
            patch("mastermind.gamemode.human.display", return_value="1234"),
            patch("mastermind.gamemode.human.console") as console,
            patch("mastermind.gamemode.human.pause"),
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            prompt.side_effect = ["1111", "1234"]

            from mastermind.gamemode.human import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "tries" in printed  # plural: "2 tries"

    def test_out_of_tries_shows_secret(self):
        with (
            patch("mastermind.gamemode.human.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.human.ask_secret") as ask_secret,
            patch("mastermind.gamemode.human.Prompt.ask") as prompt,
            patch(
                "mastermind.gamemode.human.Feedback",
                _fake_feedback(side_effect=[_fb(0, 0), _fb(1, 0)]),
            ),
            patch("mastermind.gamemode.human.parse_code", return_value=42),
            patch("mastermind.gamemode.human.display", return_value="5555"),
            patch("mastermind.gamemode.human.console") as console,
            patch("mastermind.gamemode.human.pause") as pause,
        ):
            ask_settings.return_value = (6, 4, 2)
            ask_secret.return_value = 0
            prompt.side_effect = ["1111", "2222"]

            from mastermind.gamemode.human import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Out of tries" in printed or "✗" in printed
            assert "5555" in printed
            pause.assert_called_once()

    def test_invalid_guess_retried(self):
        with (
            patch("mastermind.gamemode.human.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.human.ask_secret") as ask_secret,
            patch("mastermind.gamemode.human.Prompt.ask") as prompt,
            patch("mastermind.gamemode.human.Feedback", _fake_feedback(_fb(4, 0))),
            patch("mastermind.gamemode.human.parse_code") as parse_code,
            patch("mastermind.gamemode.human.display", return_value="1234"),
            patch("mastermind.gamemode.human.console") as console,
            patch("mastermind.gamemode.human.pause"),
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            prompt.side_effect = ["bad", "1234"]
            parse_code.side_effect = [None, 42]

            from mastermind.gamemode.human import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Invalid" in printed
            assert prompt.call_count == 2

    def test_feedback_printed_each_turn(self):
        with (
            patch("mastermind.gamemode.human.ask_game_settings") as ask_settings,
            patch("mastermind.gamemode.human.ask_secret") as ask_secret,
            patch("mastermind.gamemode.human.Prompt.ask") as prompt,
            patch(
                "mastermind.gamemode.human.Feedback",
                _fake_feedback(side_effect=[_fb(1, 2), _fb(4, 0)]),
            ),
            patch("mastermind.gamemode.human.parse_code", return_value=42),
            patch("mastermind.gamemode.human.display", return_value="1234"),
            patch("mastermind.gamemode.human.console") as console,
            patch("mastermind.gamemode.human.pause"),
        ):
            ask_settings.return_value = (6, 4, 10)
            ask_secret.return_value = 0
            prompt.side_effect = ["1111", "1234"]

            from mastermind.gamemode.human import play

            play()

            printed = " ".join(str(c) for c in console.print.call_args_list)
            assert "Feedback" in printed
