package org.mastermind.solver;

import org.junit.jupiter.api.Test;
import org.mastermind.codes.ConvertCode;

import static org.junit.jupiter.api.Assertions.*;

public class SolutionSpaceTest {

    private static final int C     = 6;
    private static final int D     = 4;
    private static final int TOTAL = 1296; // 6^4

    private static int ind(int code) { return ConvertCode.toIndex(C, D, code); }

    @Test
    void testFilterSolutionTwice() {
        int   guess1Idx        = ind(1123);
        int   guess2Idx        = ind(2456);
        int   secretIdx        = ind(4563);
        int[] colorFreqCounter = new int[C];

        int feedback1 = Feedback.getFeedback(guess1Idx, secretIdx, C, D, colorFreqCounter);
        int feedback2 = Feedback.getFeedback(guess2Idx, secretIdx, C, D, colorFreqCounter);

        // Build reference: indices consistent with both feedbacks
        int expectedCount = 0;
        for (int s = 0; s < TOTAL; s++) {
            if (Feedback.getFeedback(guess1Idx, s, C, D, colorFreqCounter) == feedback1
                    && Feedback.getFeedback(guess2Idx, s, C, D, colorFreqCounter) == feedback2) {
                expectedCount++;
            }
        }

        SolutionSpace space = new SolutionSpace(C, D);
        space.filterSolution(guess1Idx, feedback1);
        space.filterSolution(guess2Idx, feedback2);

        assertEquals(expectedCount, space.getSize());
        for (int s : space.getSecrets()) {
            assertEquals(feedback1, Feedback.getFeedback(guess1Idx, s, C, D, colorFreqCounter));
            assertEquals(feedback2, Feedback.getFeedback(guess2Idx, s, C, D, colorFreqCounter));
        }
    }

    @Test
    void testFilterSolution() {
        int   guessIdx         = ind(1123);
        int   secretIdx        = ind(4563);
        int[] colorFreqCounter = new int[C];

        // Compute the feedback for guess vs secret
        int obtainedFeedback = Feedback.getFeedback(guessIdx, secretIdx, C, D, colorFreqCounter);

        // Count how many of the 1296 indices produce the same feedback
        int expectedCount = 0;
        for (int s = 0; s < TOTAL; s++) {
            if (Feedback.getFeedback(guessIdx, s, C, D, colorFreqCounter) == obtainedFeedback) {
                expectedCount++;
            }
        }

        // filterSolution should retain exactly those indices
        SolutionSpace space = new SolutionSpace(C, D);
        assertEquals(TOTAL, space.getSize(), "Initial solution space should be 1296");

        space.filterSolution(guessIdx, obtainedFeedback);
        assertEquals(expectedCount, space.getSize(),
                     "After filtering, size should match manual count for feedback " + obtainedFeedback);

        // Every remaining secret index must produce the same feedback with the guess
        for (int s : space.getSecrets()) {
            int fb = Feedback.getFeedback(guessIdx, s, C, D, colorFreqCounter);
            assertEquals(obtainedFeedback, fb,
                         "Remaining secret index " + s + " should produce feedback " + obtainedFeedback);
        }
    }
}
