import random

from jpype.types import JInt
from mastermind.jvm import ConvertCode, Feedback
from mastermind.ui import console, pause
from rich.prompt import Prompt
from rich.rule import Rule

C = 6
D = 4
MAX_TRIES = 10


def _parse_guess(raw: str) -> int | None:
    """Return the index of the guess, or None if invalid."""
    raw = raw.strip()

    if len(raw) != D or not raw.isdigit():
        return None

    for ch in raw:
        if not (1 <= int(ch) <= C):
            return None

    return int(ConvertCode.toIndex(C, D, int(raw)))


def _display(index: int) -> str:
    return str(int(ConvertCode.toCode(C, D, index)))


def play():
    console.print()
    console.print(Rule("[bold]Mastermind (Play)[/bold]"))
    console.print(Rule(f"[dim]c={C}  d={D}  tries={MAX_TRIES}[/dim]", style="dim"))
    console.print()

    choice = Prompt.ask(
        "Who sets the secret code?\n  [bold]1)[/bold] I (computer)\n  [bold]2)[/bold] You (playing with someone else)\n",
        choices=["1", "2"],
        show_choices=False,
        default="1",
        console=console,
    )

    if choice == "2":
        while True:
            raw = Prompt.ask(
                f"Enter your secret code ([cyan]{D} digits, each 1–{C}[/cyan])",
                console=console,
            )
            secret_ind = _parse_guess(raw)
            if secret_ind is not None:
                break
            console.print(
                f"  [red]! Invalid. Use exactly {D} digits, each between 1 and {C}.[/red]"
            )
        console.print("\n[green]Code set.[/green] Hand the keyboard to the guesser!\n")

    else:
        total_codes = C**D
        secret_ind = random.randrange(total_codes)
        console.print("\nI have set a secret code. Go ahead and guess it.\n")

    color_freq: list[int] = JInt[C]
    won = False

    attempt = 0
    for attempt in range(1, MAX_TRIES + 1):
        while True:
            raw = Prompt.ask(f"▸ Guess {attempt}/{MAX_TRIES}", console=console)
            guess_ind = _parse_guess(raw)
            if guess_ind is not None:
                break
            console.print(
                f"  [red]! Invalid. Use exactly {D} digits, each between 1 and {C}.[/red]"
            )

        feedback = int(Feedback.getFeedback(guess_ind, secret_ind, C, D, color_freq))
        black = feedback // 10
        white = feedback % 10

        console.print(f"  Feedback: [bold]{black} black[/bold], {white} white\n")

        if black == D:
            won = True
            break

    if won:
        console.print(
            f"[bold green]✓ Congratulations! You cracked the code in {attempt} {'tries' if attempt != 1 else 'try'}![/bold green]\n"
        )
    else:
        console.print(
            f"[red]✗ Out of tries![/red] The secret code was: [cyan]{_display(secret_ind)}[/cyan]\n"
        )
    pause()


if __name__ == "__main__":
    play()
