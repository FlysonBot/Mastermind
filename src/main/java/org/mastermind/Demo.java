package org.mastermind;

import org.mastermind.solver.BestGuess;
import org.mastermind.solver.ExpectedSize;
import org.mastermind.solver.Feedback;

/**
 * Demo: auto-solves a single Mastermind game and prints each turn.
 * <p>
 * Defaults can be overridden at runtime:
 * java Demo <c> <d> <secret>
 * <p>
 * Examples:
 * java Demo              # uses defaults below
 * java Demo 6 4 1234     # c=6, d=4, secret=1234
 */
public class Demo {

    // ── Adjust these defaults as needed ──────────────────────────────────────
    static int C      = 9;     // number of colors
    static int D      = 9;     // number of digit positions
    static int SECRET = 641899762;  // the secret the solver tries to crack
    // ─────────────────────────────────────────────────────────────────────────

    public static void main(String[] args) {
        if (args.length >= 3) {
            C = Integer.parseInt(args[0]);
            D = Integer.parseInt(args[1]);
            SECRET = Integer.parseInt(args[2]);
        }

        System.out.printf("Mastermind Demo  [c=%d, d=%d, secret=%d]%n%n", C, D, SECRET);

        long              startTime        = System.nanoTime();
        MastermindSession session          = new MastermindSession(C, D);
        ExpectedSize      expectedSizeObj  = new ExpectedSize(D);
        int[]             colorFreqCounter = new int[10];

        while (!session.isSolved()) {
            int    spaceBefore = session.getSolutionSpaceSize();
            long[] details     = session.suggestGuessWithDetails();
            int    guess       = (int) details[0];
            float expSize = expectedSizeObj.convertSampleRankToExpectedSize(details[1], (int) details[2],
                                                                            spaceBefore);
            int feedback = Feedback.getFeedback(guess, SECRET, C, D, colorFreqCounter);

            session.recordGuess(guess, feedback);

            int turn  = session.getTurnCount();
            int black = feedback / 10;
            int white = feedback % 10;
            System.out.printf("Turn %d: guess=%-6d  space=%-5d  expected=%.2f  feedback=%db%dw%n",
                              turn, guess, spaceBefore, expSize, black, white);
        }

        double elapsedSec = (System.nanoTime() - startTime) / 1_000_000_000.0;
        System.out.printf("%nSolved in %d turn(s).%n", session.getTurnCount());
        System.out.printf("Time: %.1f seconds%n", elapsedSec);
        BestGuess.shutdown();
    }
}
