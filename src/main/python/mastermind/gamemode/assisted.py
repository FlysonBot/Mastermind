import jpype
from jpype.types import JInt
from mastermind.jvm import ConvertCode, MastermindSession

C = 6
D = 4
MAX_TRIES = 10


def _parse_code(raw: str) -> int | None:
    raw = raw.strip()
    if len(raw) != D or not raw.isdigit():
        return None
    for ch in raw:
        if not (1 <= int(ch) <= C):
            return None
    return int(ConvertCode.toIndex(C, D, int(raw)))


def _parse_feedback(raw: str) -> int | None:
    """Parse 'XbYw' or 'X Y' into feedback int (black*10 + white)."""
    raw = raw.strip().lower().replace(" ", "")
    # Accept formats: "2b1w", "21", "2b1", "2 1"
    import re
    m = re.fullmatch(r"(\d)b?(\d)w?", raw)
    if not m:
        return None
    black, white = int(m.group(1)), int(m.group(2))
    if black + white > D or black < 0 or white < 0:
        return None
    return black * 10 + white


def _display(index: int) -> str:
    return str(int(ConvertCode.toCode(C, D, index)))


def play():
    print(f"=== Mastermind Assistant  [c={C}, d={D}, tries={MAX_TRIES}] ===\n")
    print("I'll suggest the best guess each turn.")
    print("Enter the guess you actually played (or press Enter to use my suggestion),")
    print("then enter the feedback you received.\n")

    session = MastermindSession(C, D)
    color_freq: list[int] = JInt[C]

    for attempt in range(1, MAX_TRIES + 1):
        suggestion_ind = int(session.suggestGuess())
        suggestion_str = _display(suggestion_ind)
        print(f"Turn {attempt}/{MAX_TRIES}  —  Suggested guess: {suggestion_str}")

        # Ask what guess was actually played
        while True:
            raw = input(f"  Your guess (Enter = {suggestion_str}): ").strip()
            if raw == "":
                guess_ind = suggestion_ind
                break
            guess_ind = _parse_code(raw)
            if guess_ind is not None:
                break
            print(f"  Invalid. Use exactly {D} digits, each between 1 and {C}.")

        # Ask for feedback
        while True:
            raw = input("  Feedback (blacks whites, e.g. '2b1w' or '2 1'): ")
            feedback = _parse_feedback(raw)
            if feedback is not None:
                break
            print("  Invalid. Enter blacks and whites, e.g. '2b1w', '21', or '2 1'.")

        black = feedback // 10
        white = feedback % 10

        if black == D:
            session.recordGuess(guess_ind, feedback)
            print(f"\nPerfect! Solved in {attempt} {'tries' if attempt != 1 else 'try'}!")
            return

        try:
            session.recordGuess(guess_ind, feedback)
        except jpype.JException as e:
            if "No valid secrets remain" in str(e):
                print("\nNo valid codes match the feedback history — your inputs may be inconsistent.")
                print("Please double-check your guesses and feedback, then start over.")
            else:
                raise
            return

        remaining = session.getSolutionSpaceSize()
        print(f"  ({remaining} possible code{'s' if remaining != 1 else ''} remaining)\n")

    print(f"\nOut of turns. The algorithm could not determine the code — try again from the start.")


if __name__ == "__main__":
    play()
