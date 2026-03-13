import random

from mastermind.ui.console import console
from mastermind.ui.convert_code import parse_code
from rich.prompt import IntPrompt, Prompt


def ask_game_settings() -> tuple[int, int, int]:
    """Ask for colors, digits, and max tries. Returns (c, d, max_tries)."""

    while True:
        c = IntPrompt.ask("  Colors (1–9)", default=6, console=console)
        if 1 <= c <= 9:
            break
        console.print("  [red]! Must be between 1 and 9.[/red]")

    while True:
        d = IntPrompt.ask("  Digits (1–9)", default=4, console=console)
        if 1 <= d <= 9:
            break
        console.print("  [red]! Must be between 1 and 9.[/red]")

    while True:
        max_tries = IntPrompt.ask("  Max tries", default=10, console=console)
        if max_tries >= 1:
            break
        console.print("  [red]! Must be at least 1.[/red]")

    return c, d, max_tries


def ask_secret(c: int, d: int, human_follow_up: str, computer_follow_up: str) -> int:
    """
    Ask who sets the secret code and return the secret index.

    human_follow_up    — message printed after the human enters a valid code
    computer_follow_up — message printed after the computer picks a code
    """
    choice = Prompt.ask(
        "Who sets the secret code?\n  [bold]1)[/bold] Computer\n  [bold]2)[/bold] Human\n",
        choices=["1", "2"],
        show_choices=False,
        default="1",
        console=console,
    )

    if choice == "2":
        while True:
            raw = Prompt.ask(
                f"Enter your secret code ([cyan]{d} digits, each 1–{c}[/cyan], hidden)",
                password=True,
                console=console,
            )
            secret_ind = parse_code(raw, c, d)
            if secret_ind is not None:
                break
            console.print(
                f"  [red]! Invalid. Use exactly {d} digits, each between 1 and {c}.[/red]"
            )
        console.print(human_follow_up)
    else:
        secret_ind = random.randrange(c**d)
        console.print(computer_follow_up)

    return secret_ind
