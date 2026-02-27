package org.mastermind.solver;

import org.junit.jupiter.api.Test;
import org.mastermind.codes.CodeCache;

import static org.junit.jupiter.api.Assertions.*;

public class SolutionSpaceTest {

    private static final int C     = 6;
    private static final int D     = 4;
    private static final int TOTAL = 1296; // 6^4

    @Test
    void testFilterSolution() {
        int   guess            = 1123;
        int   secret           = 4563;
        int[] colorFreqCounter = new int[10];

        // Compute the feedback for guess vs secret
        int obtainedFeedback = Feedback.getFeedback(guess, secret, D, colorFreqCounter);

        // Count how many of the 1296 codes produce the same feedback
        int[] allCodes      = CodeCache.getAllValid(C, D);
        int   expectedCount = 0;
        for (int s : allCodes) {
            if (Feedback.getFeedback(guess, s, D, colorFreqCounter) == obtainedFeedback) {
                expectedCount++;
            }
        }

        // filterSolution should retain exactly those codes
        SolutionSpace space = new SolutionSpace(C, D);
        assertEquals(TOTAL, space.getSize(), "Initial solution space should be 1296");

        space.filterSolution(guess, obtainedFeedback);
        assertEquals(expectedCount, space.getSize(),
                     "After filtering, size should match manual count for feedback " + obtainedFeedback);

        // Every remaining secret must produce the same feedback with the guess
        for (int s : space.getSecrets()) {
            int fb = Feedback.getFeedback(guess, s, D, colorFreqCounter);
            assertEquals(obtainedFeedback, fb,
                         "Remaining secret " + s + " should produce feedback " + obtainedFeedback);
        }
    }
}
