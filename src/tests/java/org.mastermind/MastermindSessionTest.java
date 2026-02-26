package org.mastermind;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class MastermindSessionTest {

    private static final int C = 6;
    private static final int D = 4;
    private static final int MAX_TURNS = 6;

    /**
     * Simulate a full game with secret 1234 (a typical canonical starting case).
     * The solver must finish within MAX_TURNS turns.
     */
    @Test
    void testSolveSecret1234() {
        runGame(1234);
    }

    /**
     * Simulate a full game with secret 6666 (all same color, worst-case candidate).
     */
    @Test
    void testSolveSecret6666() {
        runGame(6666);
    }

    /**
     * Simulate a full game with secret 1562 (arbitrary mid-range code).
     */
    @Test
    void testSolveSecret1562() {
        runGame(1562);
    }

    private void runGame(int secret) {
        MastermindSession session = new MastermindSession(C, D);
        int[] colorFreqCounter = new int[10];
        ExpectedSize expectedSize = new ExpectedSize(D);
        int[] feedbackFreq = new int[100];

        System.out.println("Secret: " + secret);

        while (!session.isSolved()) {
            assertFalse(session.getTurnCount() >= MAX_TURNS,
                    "Solver exceeded " + MAX_TURNS + " turns for secret " + secret
                    + " (still unsolved after turn " + session.getTurnCount() + ")");

            int spaceBefore = session.getSolutionSpaceSize();
            int guess = session.suggestGuess();
            float expSize = expectedSize.calcExpectedSize(guess, session.getSolutionSpaceSecrets(), D, feedbackFreq);

            int feedback = Feedback.getFeedback(guess, secret, D, colorFreqCounter);
            session.recordGuess(guess, feedback);

            int turn = session.getTurnCount();
            int black = feedback / 10;
            int white = feedback % 10;
            System.out.printf("  Turn %d: guess=%d  space=%d  expected=%.2f  feedback=%db%dw%n",
                    turn, guess, spaceBefore, expSize, black, white);
        }

        System.out.println("  Solved in " + session.getTurnCount() + " turns.");

        assertTrue(session.isSolved(), "Game should be marked solved");
        assertTrue(session.getTurnCount() <= MAX_TURNS,
                "Should solve within " + MAX_TURNS + " turns, took " + session.getTurnCount());
    }
}
