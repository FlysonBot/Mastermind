from mastermind.ui.console import console, pause
from rich.console import Group
from rich.panel import Panel
from rich.rule import Rule


def show_rules():
    console.print()
    console.print(
        Panel(
            Group(
                Rule("[bold]OVERVIEW[/bold]", style="dim"),
                (
                    "\n Mastermind is a code-breaking game for two players: a"
                    "\n [red]code-setter[/red] and a [red]code-breaker[/red]."
                    "\n"
                    "\n   ▸ The [red]code-setter[/red] picks a secret code — a sequence of"
                    "\n     colored pegs (here represented as digits 1–6)."
                    "\n   ▸ The [red]code-breaker[/red] tries to guess it in as few attempts"
                    "\n     as possible, using feedback after each guess."
                    "\n"
                ),
                Rule("[bold]THE CODE[/bold]", style="dim"),
                (
                    "\n A code is a sequence of 4 digits, each between 1 and 6."
                    "\n Repetition is allowed."
                    "\n"
                    "\n   Examples of valid codes:  [cyan]1234   6611   3333   2416[/cyan]"
                    "\n"
                ),
                Rule("[bold]THE GOAL[/bold]", style="dim"),
                (
                    "\n The [red]code-breaker[/red] wins by guessing the exact secret code"
                    "\n within 10 tries. If they run out of tries, the [red]code-setter[/red]"
                    "\n wins and the secret is revealed."
                    "\n"
                ),
                Rule("[bold]FEEDBACK: BLACKS AND WHITES[/bold]", style="dim"),
                (
                    "\n After each guess, the [red]code-setter[/red] gives feedback using two"
                    "\n numbers:"
                    "\n"
                    "\n   [bold #ffffff on #1a1a1a]BLACK[/bold #ffffff on #1a1a1a]  — a digit is the correct color AND in the correct"
                    "\n             position."
                    "\n   [bold #1a1a1a on #f0f0f0]WHITE[/bold #1a1a1a on #f0f0f0]  — a digit is the correct color but in the WRONG"
                    "\n             position."
                    "\n"
                    "\n A digit can only be counted once. Blacks take priority."
                    "\n"
                ),
                Rule("[dim]Example 1[/dim]", style="dim"),
                (
                    "\n   Secret:  1 2 3 4"
                    "\n   Guess:   1 3 5 4"
                    "\n"
                    "\n   Position 1: guess=1, secret=1  → [bold #ffffff on #1a1a1a]BLACK[/bold #ffffff on #1a1a1a]  [green]✓[/green] (right place)"
                    "\n   Position 2: guess=3, secret=2  → 3 is not in the secret at all"
                    "\n   Position 3: guess=5, secret=3  → 5 is not in the secret at all"
                    "\n   Position 4: guess=4, secret=4  → [bold #ffffff on #1a1a1a]BLACK[/bold #ffffff on #1a1a1a]  [green]✓[/green] (right place)"
                    "\n   The 3 from position 2 is not in the secret, so no white."
                    "\n"
                    "\n   Feedback:  2 black,  0 white"
                    "\n"
                ),
                Rule("[dim]Example 2[/dim]", style="dim"),
                (
                    "\n   Secret:  1 2 3 4"
                    "\n   Guess:   4 1 2 6"
                    "\n"
                    "\n   Position 1: guess=4, secret=1  → 4 is elsewhere (pos 4) → [bold #1a1a1a on #f0f0f0]WHITE[/bold #1a1a1a on #f0f0f0]"
                    "\n   Position 2: guess=1, secret=2  → 1 is elsewhere (pos 1) → [bold #1a1a1a on #f0f0f0]WHITE[/bold #1a1a1a on #f0f0f0]"
                    "\n   Position 3: guess=2, secret=3  → 2 is elsewhere (pos 2) → [bold #1a1a1a on #f0f0f0]WHITE[/bold #1a1a1a on #f0f0f0]"
                    "\n   Position 4: guess=6, secret=4  → 6 not in secret"
                    "\n"
                    "\n   Feedback:  0 black,  3 white"
                    "\n"
                ),
                Rule("[dim]Example 3[/dim]", style="dim"),
                (
                    "\n   Secret:  1 1 2 3"
                    "\n   Guess:   1 4 1 5"
                    "\n"
                    "\n   Position 1: guess=1, secret=1  → [bold #ffffff on #1a1a1a]BLACK[/bold #ffffff on #1a1a1a]  [green]✓[/green]"
                    "\n   Position 2: guess=4, secret=1  → 4 not in secret"
                    "\n   Position 3: guess=1, secret=2  → there is a second 1 in the"
                    "\n                                     secret (pos 2), so → [bold #1a1a1a on #f0f0f0]WHITE[/bold #1a1a1a on #f0f0f0]"
                    "\n   Position 4: guess=5, secret=3  → 5 not in secret"
                    "\n"
                    "\n   Feedback:  1 black,  1 white"
                    "\n"
                    "\n   Notice: the secret has two 1s, but one was already matched"
                    "\n   black, so only one remaining 1 in the secret can pair with"
                    "\n   the unmatched 1 in the guess."
                    "\n"
                ),
                Rule("[bold]STRATEGY TIPS[/bold]", style="dim"),
                (
                    "\n   ▸ A feedback of 0 black, 0 white means none of your guessed"
                    "\n     digits appear in the secret at all — very useful!"
                    "\n   ▸ Use early guesses to test many different digits at once."
                    "\n   ▸ Narrow down positions with follow-up guesses based on the"
                    "\n     white clues you receive."
                    "\n"
                ),
                Rule("[bold]WINNING AND LOSING[/bold]", style="dim"),
                (
                    "\n   ▸ 4 black, 0 white = perfect guess → [green]you win![/green]"
                    "\n   ▸ Guess correctly within 10 tries → [red]code-breaker[/red] wins."
                    "\n   ▸ Fail to guess within 10 tries   → [red]code-setter[/red] wins,"
                    "\n     and the secret is revealed."
                    "\n"
                ),
                "\n [bold blue]Good luck![/bold blue]",
            ),
            title="[bold]HOW TO PLAY MASTERMIND[/bold]",
            highlight=True,
        )
    )
    console.print()
    pause()


if __name__ == "__main__":
    show_rules()
