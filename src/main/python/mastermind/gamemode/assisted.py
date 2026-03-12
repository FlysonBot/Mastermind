import re

import jpype
from mastermind.jvm import MastermindSession
from mastermind.ui import console, pause
from mastermind.ui.convert_code import display, parse_code
from rich.prompt import Prompt
from rich.rule import Rule

C = 6
D = 4
MAX_TRIES = 10


def _parse_feedback(raw: str) -> int | None:
    """Parse 'XbYw' or 'X Y' into feedback int (black*10 + white)."""
    raw = raw.strip().lower().replace(" ", "")
    # Accept formats: "2b1w", "21", "2b1", "2 1"
    m = re.fullmatch(r"(\d)b?(\d)w?", raw)
    if not m:
        return None

    black, white = int(m.group(1)), int(m.group(2))
    if black + white > D or black < 0 or white < 0:
        return None

    return black * 10 + white


def play():
    console.print()
    console.print(Rule("[bold]Mastermind (Assist)[/bold]"))
    console.print(Rule(f"[dim]c={C}  d={D}  tries={MAX_TRIES}[/dim]", style="dim"))
    console.print()
    console.print("I'll suggest the best guess each turn.")
    console.print(
        "Enter the guess you actually played (or press Enter to use my suggestion),"
    )
    console.print("then enter the feedback you received.\n")

    session = MastermindSession(C, D)

    for attempt in range(1, MAX_TRIES + 1):
        suggestion_ind = int(session.suggestGuess())
        suggestion_str = display(suggestion_ind, C, D)
        console.print(
            f"\n▸ Turn {attempt}/{MAX_TRIES}  —  💡 Suggested guess: [cyan]{suggestion_str}[/cyan]"
        )

        # Ask what guess was actually played
        while True:
            raw = Prompt.ask(
                "  Your guess",
                default=suggestion_str,
                console=console,
            )
            if raw == suggestion_str:
                guess_ind = suggestion_ind
                break

            guess_ind = parse_code(raw, C, D)
            if guess_ind is not None:
                break

            console.print(
                f"  [red]! Invalid. Use exactly {D} digits, each between 1 and {C}.[/red]"
            )

        # Ask for feedback
        while True:
            raw = Prompt.ask(
                "  Feedback (blacks whites, e.g. '2b1w' or '2 1')", console=console
            )
            feedback = _parse_feedback(raw)
            if feedback is not None:
                break

            console.print(
                "  [red]! Invalid. Enter blacks and whites, e.g. '2b1w', '21', or '2 1'.[/red]"
            )

        black = feedback // 10

        if black == D:
            session.recordGuess(guess_ind, feedback)
            console.print(
                f"\n[bold green]✓ Perfect! Solved in {attempt} {'tries' if attempt != 1 else 'try'}![/bold green]\n"
            )
            pause()
            return

        try:
            session.recordGuess(guess_ind, feedback)

        except jpype.JException as e:
            if "No valid secrets remain" in str(e):
                console.print(
                    "\n[red]✗ No valid codes match the feedback history — your inputs may be inconsistent.[/red]"
                )
                console.print(
                    "Please double-check your guesses and feedback, then start over.\n"
                )
            else:
                raise

            pause()
            return

        remaining = session.getSolutionSpaceSize()
        console.print(
            f"  [dim]({remaining} possible code{'s' if remaining != 1 else ''} remaining)[/dim]\n"
        )

    console.print(
        "\n[red]✗ Out of turns. The algorithm could not determine the code — try again from the start.[/red]\n"
    )
    pause()


if __name__ == "__main__":
    play()
