import random
from jpype.types import JInt
from mastermind.jvm import ConvertCode, Feedback

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
    print(f"=== Mastermind  [c={C}, d={D}, tries={MAX_TRIES}] ===\n")
    print(f"Colors: 1–{C},  Code length: {D} digits\n")

    choice = input("Who sets the secret code?\n  1) I (computer)\n  2) You (playing with someone else)\n> ").strip()

    if choice == "2":
        while True:
            raw = input(f"Enter your secret code ({D} digits, each 1–{C}): ").strip()

            secret_ind = _parse_guess(raw)
            if secret_ind is not None:
                break

            print(f"  Invalid. Use exactly {D} digits, each between 1 and {C}.")
        print("\nCode set. Hand the keyboard to the guesser!\n")

    else:
        total_codes = C ** D
        secret_ind = random.randrange(total_codes)
        print("I have set a secret code. Go ahead and guess it.\n")

    color_freq: list[int] = JInt[C]
    won = False

    attempt = 0
    for attempt in range(1, MAX_TRIES + 1):
        while True:
            raw = input(f"Guess {attempt}/{MAX_TRIES}: ").strip()

            guess_ind = _parse_guess(raw)
            if guess_ind is not None:
                break

            print(f"  Invalid. Use exactly {D} digits, each between 1 and {C}.")

        feedback = int(Feedback.getFeedback(guess_ind, secret_ind, C, D, color_freq))
        black = feedback // 10
        white = feedback % 10

        print(f"  Feedback: {black} black, {white} white")

        if black == D:
            won = True
            break

    print()
    if won:
        print(f"Congratulations! You cracked the code in {attempt} {'tries' if attempt != 1 else 'try'}!\n\n")
    else:
        print(f"Out of tries! The secret code was: {_display(secret_ind)}\n\n")


if __name__ == "__main__":
    play()
