from jpype.types import JInt
from mastermind.jvm import Feedback, MastermindSession
from mastermind.ui import console, pause
from mastermind.ui.convert_code import display
from mastermind.ui.prompts import ask_game_settings, ask_secret
from rich.rule import Rule


def play():
    console.print()
    console.print(Rule("[bold]Mastermind (Watch)[/bold]"))
    console.print()

    c, d, max_tries = ask_game_settings()
    console.print(Rule(f"[dim]c={c}  d={d}  tries={max_tries}[/dim]", style="dim"))
    console.print()

    secret_ind = ask_secret(
        c,
        d,
        human_follow_up="\n[green]Code set.[/green] Watch the computer solve it!\n",
        computer_follow_up="\nI have set a secret code. Now I will solve it...\n",
    )

    session = MastermindSession(c, d)
    color_freq: list[int] = JInt[c]

    for attempt in range(1, max_tries + 1):
        guess_ind = int(session.suggestGuess())
        feedback = int(Feedback.getFeedback(guess_ind, secret_ind, c, d, color_freq))
        black = feedback // 10
        white = feedback % 10

        console.print(
            f"  ▸ Guess {attempt}/{max_tries}: [cyan]{display(guess_ind, c, d)}[/cyan]"
            f"  →  [bold]{black} black[/bold], {white} white"
        )

        session.recordGuess(guess_ind, feedback)

        if black == d:
            console.print(
                f"\n[bold green]✓ I solved it in {attempt} {'tries' if attempt != 1 else 'try'}![/bold green]\n"
            )
            pause()
            return

    console.print(
        f"\n[red]✗ I failed to solve it within {max_tries} tries.[/red]"
        f" The secret was: [cyan]{display(secret_ind, c, d)}[/cyan]\n"
    )
    pause()


if __name__ == "__main__":
    play()
