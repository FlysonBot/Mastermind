package org.mastermind;

import org.junit.jupiter.api.Test;
import org.mastermind.codes.ConvertCode;
import org.mastermind.compute.ExpectedSize;
import org.mastermind.compute.Feedback;
import org.mastermind.solver.BestFirstGuess;

import static org.junit.jupiter.api.Assertions.*;

public class MastermindSessionTest {

    private static final int C         = 6;
    private static final int D         = 4;
    private static final int MAX_TURNS = 6;

    private static int ind(int code) { return ConvertCode.toIndex(C, D, code); }

    /**
     * Simulate a full game with secret 1234 (a typical canonical starting case).
     * The solver must finish within MAX_TURNS turns.
     */
    @Test
    void testSolveSecret1234() {
        runGame(ind(1234));
    }

    /** Simulate a full game with secret 6666 (all same color, worst-case candidate). */
    @Test
    void testSolveSecret6666() {
        runGame(ind(6666));
    }

    /**
     * On an empty history, suggestGuessWithDetails should return the precomputed
     * best first guess with the correct rank and the full solution space size.
     */
    @Test
    void testSuggestGuessWithDetailsOnEmptyHistory() {
        MastermindSession session = new MastermindSession(C, D);
        long[]            details = session.suggestGuessWithDetails();

        long[] best          = BestFirstGuess.of(C, D);
        int    expectedGuess = ConvertCode.toIndex(C, D, (int) best[0]);
        long   expectedRank  = best[1];
        int    expectedSpace = (int) Math.pow(C, D);

        assertEquals(expectedGuess, details[0], "First guess index should match BestFirstGuess table");
        assertEquals(expectedRank, details[1], "Rank should match precomputed BestFirstGuess rank");
        assertEquals(expectedSpace, details[2], "Secrets length should be the full solution space");
    }

    /** Simulate a full game with secret 1562 (arbitrary mid-range code). */
    @Test
    void testSolveSecret1562() {
        runGame(ind(1562));
    }

    /** Record two guesses, undo both at once, and verify the session is fully reset. */
    @Test
    void testUndoMultiple() {
        int[]             colorFreqCounter = new int[C];
        MastermindSession session          = new MastermindSession(C, D);

        int spaceAtStart = session.getSolutionSpaceSize();

        // Record two arbitrary guesses with their real feedbacks against secret 1234
        int guess1 = ind(1122);
        int fb1    = Feedback.getFeedback(guess1, ind(1234), C, D, colorFreqCounter);
        session.recordGuess(guess1, fb1);
        int spaceAfter1 = session.getSolutionSpaceSize();

        int guess2 = ind(1344);
        int fb2    = Feedback.getFeedback(guess2, ind(1234), C, D, colorFreqCounter);
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
        int[]             colorFreqCounter = new int[C];
        MastermindSession session          = new MastermindSession(C, D);

        int guess1 = ind(1122);
        int fb1    = Feedback.getFeedback(guess1, ind(1234), C, D, colorFreqCounter);
        session.recordGuess(guess1, fb1);
        int spaceAfter1 = session.getSolutionSpaceSize();

        int guess2 = ind(1344);
        int fb2    = Feedback.getFeedback(guess2, ind(1234), C, D, colorFreqCounter);
        session.recordGuess(guess2, fb2);

        int guess3 = ind(1234);
        int fb3    = Feedback.getFeedback(guess3, ind(1234), C, D, colorFreqCounter);
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

    private void runGame(int secretInd) {
        MastermindSession session      = new MastermindSession(C, D);
        int[]             colorFreq    = new int[C];
        ExpectedSize      expectedSize = new ExpectedSize(D);
        int[]             feedbackFreq = new int[100];

        System.out.println("Secret index: " + secretInd);

        while (!session.isSolved()) {
            assertFalse(session.getTurnCount() >= MAX_TURNS,
                        "Solver exceeded " + MAX_TURNS + " turns for secret " + secretInd
                                + " (still unsolved after turn " + session.getTurnCount() + ")");

            int spaceBefore = session.getSolutionSpaceSize();
            int guessInd    = session.suggestGuess();
            float expSize = expectedSize.calcExpectedSize(guessInd, session.getSolutionSpaceSecrets(), C, D,
                                                          feedbackFreq);

            int feedback = Feedback.getFeedback(guessInd, secretInd, C, D, colorFreq);
            session.recordGuess(guessInd, feedback);

            int turn  = session.getTurnCount();
            int black = feedback / 10;
            int white = feedback % 10;
            System.out.printf("  Turn %d: guessInd=%d  space=%d  expected=%.2f  feedback=%db%dw%n",
                              turn, guessInd, spaceBefore, expSize, black, white);
        }

        System.out.println("  Solved in " + session.getTurnCount() + " turns.");

        assertTrue(session.isSolved(), "Game should be marked solved");
        assertTrue(session.getTurnCount() <= MAX_TURNS,
                   "Should solve within " + MAX_TURNS + " turns, took " + session.getTurnCount());
    }
}
