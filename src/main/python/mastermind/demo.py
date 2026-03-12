import sys
import time

from jpype.types import JInt
from mastermind.jvm import ConvertCode, ExpectedSize, Feedback, MastermindSession
from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()

# ── Adjust these settings as needed ──────────────────────────────────────
C = 9
D = 9
SECRET_IND = 641899762  # index of the secret code (0-based, base-c encoding)
# ─────────────────────────────────────────────────────────────────────────


def demo():
    c, d, secret_ind = C, D, SECRET_IND

    if len(sys.argv) >= 4:
        c = int(sys.argv[1])
        d = int(sys.argv[2])
        secret_ind = int(sys.argv[3])

    console.print(
        f"\n[bold]Mastermind Demo[/bold]  c={c}, d={d}, secretInd={secret_ind}\n"
    )

    table = Table(highlight=True)
    table.add_column("Turn", justify="right")
    table.add_column("Size Before", justify="right")
    table.add_column("Exp After", justify="right")
    table.add_column("Act After", justify="right")
    table.add_column("Exp Elim%", justify="right")
    table.add_column("Act Elim%", justify="right")
    table.add_column("Guess", justify="center", style="cyan")
    table.add_column("Result", justify="center")
    table.add_column("Suggest (s)", justify="right")
    table.add_column("Record (s)", justify="right")

    start = time.perf_counter()
    session = MastermindSession(c, d)
    exp_size = ExpectedSize(d)
    color_freq: list[int] = JInt[c]

    with Live(table, console=console, refresh_per_second=10):
        while not session.isSolved():
            space_before = session.getSolutionSpaceSize()

            t0 = time.perf_counter()
            details = session.suggestGuessWithDetails()
            t_suggest = time.perf_counter() - t0

            guess_ind = int(details[0])
            exp = exp_size.convertSampleRankToExpectedSize(
                details[1], int(details[2]), space_before
            )
            feedback = Feedback.getFeedback(guess_ind, secret_ind, c, d, color_freq)

            t0 = time.perf_counter()
            session.recordGuess(guess_ind, feedback)
            t_record = time.perf_counter() - t0

            turn = session.getTurnCount()
            space_after = session.getSolutionSpaceSize()
            black = int(feedback) // 10
            white = int(feedback) % 10
            exp_elim = (
                100 * (space_before - float(exp)) / space_before
                if space_before > 0
                else 0.0
            )
            act_elim = (
                100 * (space_before - space_after) / space_before
                if space_before > 0
                else 0.0
            )
            guess_code = ConvertCode.toCode(c, d, guess_ind)

            table.add_row(
                str(turn),
                str(space_before),
                f"{float(exp):.1f}",
                str(space_after),
                f"{exp_elim:.1f}%",
                f"{act_elim:.1f}%",
                str(int(guess_code)),
                f"[bold]{black}b[/bold] {white}w",
                f"{t_suggest:.3f}",
                f"{t_record:.3f}",
            )

    elapsed = time.perf_counter() - start
    console.print(
        f"\n[bold green]Solved in {session.getTurnCount()} turn(s).[/bold green]"
    )
    console.print(f"Time: {elapsed:.1f} seconds\n")


if __name__ == "__main__":
    demo()
