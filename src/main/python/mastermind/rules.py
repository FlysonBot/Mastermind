def show_rules():
    print("""
╔══════════════════════════════════════════════════════════╗
║               HOW TO PLAY MASTERMIND                     ║
╚══════════════════════════════════════════════════════════╝

OVERVIEW
────────
Mastermind is a code-breaking game for two players: a
code-setter and a code-breaker.

  • The code-setter picks a secret code — a sequence of
    colored pegs (here represented as digits 1–6).
  • The code-breaker tries to guess it in as few attempts
    as possible, using feedback after each guess.

THE CODE
────────
A code is a sequence of 4 digits, each between 1 and 6.
Repetition is allowed.

  Examples of valid codes:  1234   6611   3333   2416

THE GOAL
────────
The code-breaker wins by guessing the exact secret code
within 10 tries. If they run out of tries, the code-setter
wins and the secret is revealed.

FEEDBACK: BLACKS AND WHITES
────────────────────────────
After each guess, the code-setter gives feedback using two
numbers:

  BLACK  — a digit is the correct color AND in the correct
            position.
  WHITE  — a digit is the correct color but in the WRONG
            position.

A digit can only be counted once. Blacks take priority.

─ Example 1 ───────────────────────────────────────────────
  Secret:  1 2 3 4
  Guess:   1 3 5 4

  Position 1: guess=1, secret=1  → BLACK  ✓ (right place)
  Position 2: guess=3, secret=2  → 3 is not in the secret at all
  Position 3: guess=5, secret=3  → 5 is not in the secret at all
  Position 4: guess=4, secret=4  → BLACK  ✓ (right place)
  The 3 from position 2 is not in the secret, so no white.

  Feedback:  2 black,  0 white
───────────────────────────────────────────────────────────

─ Example 2 ───────────────────────────────────────────────
  Secret:  1 2 3 4
  Guess:   4 1 2 6

  Position 1: guess=4, secret=1  → 4 is elsewhere (pos 4) → WHITE
  Position 2: guess=1, secret=2  → 1 is elsewhere (pos 1) → WHITE
  Position 3: guess=2, secret=3  → 2 is elsewhere (pos 2) → WHITE
  Position 4: guess=6, secret=4  → 6 not in secret

  Feedback:  0 black,  3 white
───────────────────────────────────────────────────────────

─ Example 3 ───────────────────────────────────────────────
  Secret:  1 1 2 3
  Guess:   1 4 1 5

  Position 1: guess=1, secret=1  → BLACK  ✓
  Position 2: guess=4, secret=1  → 4 not in secret
  Position 3: guess=1, secret=2  → there is a second 1 in the
                                    secret (pos 2), so → WHITE
  Position 4: guess=5, secret=3  → 5 not in secret

  Feedback:  1 black,  1 white

  Notice: the secret has two 1s, but one was already matched
  black, so only one remaining 1 in the secret can pair with
  the unmatched 1 in the guess.
───────────────────────────────────────────────────────────

STRATEGY TIPS
─────────────
  • A feedback of 0 black, 0 white means none of your guessed
    digits appear in the secret at all — very useful!
  • Use early guesses to test many different digits at once.
  • Narrow down positions with follow-up guesses based on the
    white clues you receive.

WINNING AND LOSING
──────────────────
  • 4 black, 0 white = perfect guess → you win!
  • Guess correctly within 10 tries → code-breaker wins.
  • Fail to guess within 10 tries   → code-setter wins,
    and the secret is revealed.

Good luck!
""")


if __name__ == "__main__":
    show_rules()
