import sys
import time
from jpype.types import JArray, JInt
from mastermind.jvm import MastermindSession, ConvertCode, ExpectedSize, Feedback

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

    print(f"Mastermind Demo  [c={c}, d={d}, secretInd={secret_ind}]\n")

    start = time.perf_counter()
    session = MastermindSession(c, d)
    exp_size = ExpectedSize(d)
    color_freq = JArray(JInt)(c)  # type: ignore

    while not session.isSolved():
        space_before = session.getSolutionSpaceSize()
        details = session.suggestGuessWithDetails()
        guess_ind = int(details[0])
        exp = exp_size.convertSampleRankToExpectedSize(
            details[1], int(details[2]), space_before
        )
        feedback = Feedback.getFeedback(guess_ind, secret_ind, c, d, color_freq)

        session.recordGuess(guess_ind, feedback)

        turn = session.getTurnCount()
        space_after = session.getSolutionSpaceSize()
        black = int(feedback) // 10
        white = int(feedback) % 10
        exp_elim = (
            100 * (space_before - float(exp)) / space_before if space_before > 0 else 0.0
        )
        act_elim = (
            100 * (space_before - space_after) / space_before if space_before > 0 else 0.0
        )
        guess_code = ConvertCode.toCode(c, d, guess_ind)

        print(
            f"Turn {turn}:  before={space_before:<8}  expAfter={float(exp):<8.1f}  actAfter={space_after:<8}  "
            f"expElim={exp_elim:5.1f}%  actElim={act_elim:5.1f}%  "
            f"guess={int(guess_code):<12}  feedback={black}b{white}w"
        )

    elapsed = time.perf_counter() - start
    print(f"\nSolved in {session.getTurnCount()} turn(s).")
    print(f"Time: {elapsed:.1f} seconds")


if __name__ == "__main__":
    demo()
