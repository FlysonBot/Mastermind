import random

from jpype.types import JInt
from mastermind.jvm import Feedback, MastermindSession
from mastermind.ui import console, pause
from mastermind.ui.convert_code import display, parse_code
from rich.prompt import Prompt
from rich.rule import Rule

C = 6
D = 4
MAX_TRIES = 10


def play():
    console.print()
    console.print(Rule("[bold]Mastermind (Watch)[/bold]"))
    console.print(Rule(f"[dim]c={C}  d={D}  tries={MAX_TRIES}[/dim]", style="dim"))
    console.print()

    choice = Prompt.ask(
        "Who sets the secret code?\n  [bold]1)[/bold] I (computer)\n  [bold]2)[/bold] You\n",
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
            secret_ind = parse_code(raw, C, D)
            if secret_ind is not None:
                break
            console.print(
                f"  [red]! Invalid. Use exactly {D} digits, each between 1 and {C}.[/red]"
            )
        console.print("\n[green]Code set.[/green] Watch the computer solve it!\n")

    else:
        secret_ind = random.randrange(C**D)
        console.print("\nI have set a secret code. Now I will solve it...\n")

    session = MastermindSession(C, D)
    color_freq: list[int] = JInt[C]

    for attempt in range(1, MAX_TRIES + 1):
        guess_ind = int(session.suggestGuess())
        feedback = int(Feedback.getFeedback(guess_ind, secret_ind, C, D, color_freq))
        black = feedback // 10
        white = feedback % 10

        console.print(
            f"  ▸ Guess {attempt}/{MAX_TRIES}: [cyan]{display(guess_ind, C, D)}[/cyan]"
            f"  →  [bold]{black} black[/bold], {white} white"
        )

        session.recordGuess(guess_ind, feedback)

        if black == D:
            console.print(
                f"\n[bold green]✓ I solved it in {attempt} {'tries' if attempt != 1 else 'try'}![/bold green]\n"
            )
            pause()
            return

    console.print(
        f"\n[red]✗ I failed to solve it within {MAX_TRIES} tries.[/red]"
        f" The secret was: [cyan]{display(secret_ind, C, D)}[/cyan]\n"
    )
    pause()


if __name__ == "__main__":
    play()
