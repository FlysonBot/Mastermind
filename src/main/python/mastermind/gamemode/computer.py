import random
from jpype.types import JInt
from mastermind.jvm import ConvertCode, Feedback, MastermindSession

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


def _display(index: int) -> str:
    return str(int(ConvertCode.toCode(C, D, index)))


def play():
    print(f"=== Mastermind  [c={C}, d={D}, tries={MAX_TRIES}] ===\n")
    print(f"Colors: 1–{C},  Code length: {D} digits\n")

    choice = input("Who sets the secret code?\n  1) I (computer)\n  2) You\n> ").strip()

    if choice == "2":
        while True:
            raw = input(f"Enter your secret code ({D} digits, each 1–{C}): ").strip()
            secret_ind = _parse_code(raw)
            if secret_ind is not None:
                break
            print(f"  Invalid. Use exactly {D} digits, each between 1 and {C}.")
        print("\nCode set. Watch the computer solve it!\n")
    else:
        secret_ind = random.randrange(C ** D)
        print("I have set a secret code. Now I will solve it...\n")

    session = MastermindSession(C, D)
    color_freq: list[int] = JInt[C]

    for attempt in range(1, MAX_TRIES + 1):
        guess_ind = int(session.suggestGuess())
        feedback = int(Feedback.getFeedback(guess_ind, secret_ind, C, D, color_freq))
        black = feedback // 10
        white = feedback % 10

        print(f"Guess {attempt}/{MAX_TRIES}: {_display(guess_ind)}  →  {black} black, {white} white")

        session.recordGuess(guess_ind, feedback)

        if black == D:
            print(f"\nI solved it in {attempt} {'tries' if attempt != 1 else 'try'}!")
            return

    print(f"\nI failed to solve it within {MAX_TRIES} tries. The secret was: {_display(secret_ind)}")


if __name__ == "__main__":
    play()
