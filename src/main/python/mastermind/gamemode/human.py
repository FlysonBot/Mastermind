from jpype.types import JInt
from mastermind.jvm import Feedback
from mastermind.ui import console, pause
from mastermind.ui.convert_code import display, parse_code
from mastermind.ui.prompts import ask_game_settings, ask_secret
from rich.prompt import Prompt
from rich.rule import Rule


def play():
    console.print()
    console.print(Rule("[bold]Mastermind (Play)[/bold]"))
    console.print()

    c, d, max_tries = ask_game_settings()
    console.print(Rule(f"[dim]c={c}  d={d}  tries={max_tries}[/dim]", style="dim"))
    console.print()

    secret_ind = ask_secret(
        c,
        d,
        human_follow_up="\n[green]Code set.[/green] Hand the keyboard to the guesser!\n",
        computer_follow_up="\nI have set a secret code. Go ahead and guess it.\n",
    )

    color_freq: list[int] = JInt[c]
    won = False

    attempt = 0
    for attempt in range(1, max_tries + 1):
        while True:
            raw = Prompt.ask(f"▸ Guess {attempt}/{max_tries}", console=console)
            guess_ind = parse_code(raw, c, d)
            if guess_ind is not None:
                break
            console.print(
                f"  [red]! Invalid. Use exactly {d} digits, each between 1 and {c}.[/red]"
            )

        feedback = int(Feedback.getFeedback(guess_ind, secret_ind, c, d, color_freq))
        black = feedback // 10
        white = feedback % 10

        console.print(f"  Feedback: [bold]{black} black[/bold], {white} white\n")

        if black == d:
            won = True
            break

    if won:
        console.print(
            f"[bold green]✓ Congratulations! You cracked the code in {attempt} {'tries' if attempt != 1 else 'try'}![/bold green]\n"
        )
    else:
        console.print(
            f"[red]✗ Out of tries![/red] The secret code was: [cyan]{display(secret_ind, c, d)}[/cyan]\n"
        )
    pause()


if __name__ == "__main__":
    play()
