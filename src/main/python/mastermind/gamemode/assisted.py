import re

import jpype
from mastermind.jvm import MastermindSession
from mastermind.ui import console, pause
from mastermind.ui.convert_code import display, parse_code
from mastermind.ui.prompts import ask_game_settings
from rich.prompt import IntPrompt, Prompt
from rich.rule import Rule


def _parse_feedback(raw: str, d: int) -> int | None:
    """Parse 'XbYw' or 'X Y' into feedback int (black*10 + white)."""
    raw = raw.strip().lower().replace(" ", "")
    m = re.fullmatch(r"(\d)b?(\d)w?", raw)
    if not m:
        return None

    black, white = int(m.group(1)), int(m.group(2))
    if black + white > d or black < 0 or white < 0:
        return None

    return black * 10 + white


def play():
    console.print()
    console.print(Rule("[bold]Mastermind (Assist)[/bold]"))
    console.print()

    c, d, max_tries = ask_game_settings()
    console.print(Rule(f"[dim]c={c}  d={d}  tries={max_tries}[/dim]", style="dim"))
    console.print()

    console.print("I'll suggest the best guess each turn.")
    console.print(
        "Enter the guess you actually played (or press Enter to use my suggestion),"
    )
    console.print("then enter the feedback you received.")
    console.print("[dim]Enter 'u' at any prompt to undo.[/dim]\n")

    session = MastermindSession(c, d)
    prev_remaining: list[int] = [c**d]  # index 0 = before turn 1, index i = after turn i
    suggestions: dict[int, tuple[int, str]] = {}  # attempt -> (ind, str)

    attempt = 1
    while attempt <= max_tries:
        # Get or compute suggestion for this attempt
        if attempt not in suggestions:
            suggestion_ind = int(session.suggestGuess())
            suggestion_str = display(suggestion_ind, c, d)
            suggestions[attempt] = (suggestion_ind, suggestion_str)
        else:
            suggestion_ind, suggestion_str = suggestions[attempt]

        console.print(
            f"\n▸ Turn {attempt}/{max_tries}  —  💡 Suggested guess: [cyan]{suggestion_str}[/cyan]"
        )

        # Ask what guess was actually played
        guess_ind = None
        while True:
            raw = Prompt.ask(
                "  Your guess",
                default=suggestion_str,
                console=console,
            )
            if raw.strip().lower() == "u":
                if attempt == 1:
                    console.print("  [yellow]Nothing to undo.[/yellow]")
                    continue
                session.undo(1)
                suggestions.pop(attempt, None)
                attempt -= 1
                prev_remaining.pop()
                break
            if raw == suggestion_str:
                guess_ind = suggestion_ind
                break
            guess_ind = parse_code(raw, c, d)
            if guess_ind is not None:
                break
            console.print(
                f"  [red]! Invalid. Use exactly {d} digits, each between 1 and {c}.[/red]"
            )

        if guess_ind is None:
            # Rewound via 'u' at guess prompt
            continue

        # Ask for feedback
        feedback = None
        while True:
            raw = Prompt.ask(
                "  Feedback (blacks whites, e.g. '2b1w' or '2 1')", console=console
            )
            if raw.strip().lower() == "u":
                # Messed up the guess this turn — re-ask without undoing session
                console.print("  [yellow]Re-enter your guess.[/yellow]")
                break
            feedback = _parse_feedback(raw, d)
            if feedback is not None:
                break
            console.print(
                "  [red]! Invalid. Enter blacks and whites, e.g. '2b1w', '21', or '2 1'.[/red]"
            )

        if feedback is None:
            # 'u' at feedback prompt — re-ask guess for same attempt
            continue

        black = feedback // 10

        if black == d:
            session.recordGuess(guess_ind, feedback)
            console.print(
                f"\n[bold green]✓ Perfect! Solved in {attempt} {'tries' if attempt != 1 else 'try'}![/bold green]\n"
            )
            pause()
            return

        try:
            session.recordGuess(guess_ind, feedback)

        except jpype.JException as e:
            if "No valid secrets remain" not in str(e):
                raise
            attempt += 1
            console.print(
                "\n[red]✗ No valid codes match the feedback history — your inputs may be inconsistent.[/red]"
            )
            raw = Prompt.ask(
                "  Undo some guesses?",
                choices=["y", "n"],
                default="y",
                console=console,
            )
            if raw == "n":
                console.print()
                pause()
                return
            while True:
                n = IntPrompt.ask(
                    f"  How many guesses to undo (1–{attempt - 1})",
                    console=console,
                )
                if 1 <= n <= attempt - 1:
                    break
                console.print(f"  [red]! Must be between 1 and {attempt - 1}.[/red]")
            for t in range(attempt - n, attempt):
                suggestions.pop(t, None)
            session.undo(n)
            attempt -= n
            del prev_remaining[attempt:]
            continue

        remaining = session.getSolutionSpaceSize()
        eliminated = round((1 - remaining / prev_remaining[-1]) * 100)
        prev_remaining.append(remaining)
        console.print(
            f"  [dim](eliminated {eliminated}%"
            f", {remaining} possible code{'s' if remaining != 1 else ''} remaining)[/dim]\n"
        )
        attempt += 1

    console.print(
        "\n[red]✗ Out of turns. The algorithm could not determine the code — try again from the start.[/red]\n"
    )
    pause()


if __name__ == "__main__":
    play()
