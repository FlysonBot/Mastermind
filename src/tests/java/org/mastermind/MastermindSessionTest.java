package org.mastermind;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class MastermindSessionTest {

    private static final int C         = 6;
    private static final int D         = 4;
    private static final int MAX_TURNS = 6;

    /**
     * Simulate a full game with secret 1234 (a typical canonical starting case).
     * The solver must finish within MAX_TURNS turns.
     */
    @Test
    void testSolveSecret1234() {
        runGame(1234);
    }

    /** Simulate a full game with secret 6666 (all same color, worst-case candidate). */
    @Test
    void testSolveSecret6666() {
        runGame(6666);
    }

    /** Simulate a full game with secret 1562 (arbitrary mid-range code). */
    @Test
    void testSolveSecret1562() {
        runGame(1562);
    }

    /** Record two guesses, undo both at once, and verify the session is fully reset. */
    @Test
    void testUndoMultiple() {
        int[]             colorFreqCounter = new int[10];
        MastermindSession session          = new MastermindSession(C, D);

        int spaceAtStart = session.getSolutionSpaceSize();

        // Record two arbitrary guesses with their real feedbacks against secret 1234
        int guess1 = 1122;
        int fb1    = Feedback.getFeedback(guess1, 1234, D, colorFreqCounter);
        session.recordGuess(guess1, fb1);
        int spaceAfter1 = session.getSolutionSpaceSize();

        int guess2 = 1344;
        int fb2    = Feedback.getFeedback(guess2, 1234, D, colorFreqCounter);
        session.recordGuess(guess2, fb2);
        int spaceAfter2 = session.getSolutionSpaceSize();

        // Sanity: each filter should narrow the space
        assertTrue(spaceAfter1 < spaceAtStart);
        assertTrue(spaceAfter2 < spaceAfter1);
        assertEquals(2, session.getTurnCount());

        // Undo both guesses at once
        session.undo(2);

        assertEquals(0, session.getTurnCount());
        assertFalse(session.isSolved());
        assertEquals(spaceAtStart, session.getSolutionSpaceSize());
    }

    /**
     * Record three guesses, undo one, verify intermediate state matches
     * what it was after the first guess alone.
     */
    @Test
    void testUndoPartial() {
        int[]             colorFreqCounter = new int[10];
        MastermindSession session          = new MastermindSession(C, D);

        int guess1 = 1122;
        int fb1    = Feedback.getFeedback(guess1, 1234, D, colorFreqCounter);
        session.recordGuess(guess1, fb1);
        int spaceAfter1 = session.getSolutionSpaceSize();

        int guess2 = 1344;
        int fb2    = Feedback.getFeedback(guess2, 1234, D, colorFreqCounter);
        session.recordGuess(guess2, fb2);

        int guess3 = 1234;
        int fb3    = Feedback.getFeedback(guess3, 1234, D, colorFreqCounter);
        session.recordGuess(guess3, fb3);
        assertTrue(session.isSolved());

        // Undo last two guesses — should land back at the state after guess1
        session.undo(2);

        assertEquals(1, session.getTurnCount());
        assertFalse(session.isSolved());
        assertEquals(spaceAfter1, session.getSolutionSpaceSize());
        assertEquals(guess1, session.getHistory().getFirst()[0]);
        assertEquals(fb1, session.getHistory().getFirst()[1]);
    }

    /** Verify that undo throws when n is out of range. */
    @Test
    void testUndoInvalidN() {
        MastermindSession session = new MastermindSession(C, D);
        assertThrows(IllegalArgumentException.class, () -> session.undo(0));
        assertThrows(IllegalArgumentException.class, () -> session.undo(1));
    }

    private void runGame(int secret) {
        MastermindSession session          = new MastermindSession(C, D);
        int[]             colorFreqCounter = new int[10];
        ExpectedSize      expectedSize     = new ExpectedSize(D);
        int[]             feedbackFreq     = new int[100];

        System.out.println("Secret: " + secret);

        while (!session.isSolved()) {
            assertFalse(session.getTurnCount() >= MAX_TURNS,
                        "Solver exceeded " + MAX_TURNS + " turns for secret " + secret
                                + " (still unsolved after turn " + session.getTurnCount() + ")");

            int spaceBefore = session.getSolutionSpaceSize();
            int guess       = session.suggestGuess();
            float expSize = expectedSize.calcExpectedSize(guess, session.getSolutionSpaceSecrets(), D,
                                                          feedbackFreq);

            int feedback = Feedback.getFeedback(guess, secret, D, colorFreqCounter);
            session.recordGuess(guess, feedback);

            int turn  = session.getTurnCount();
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
