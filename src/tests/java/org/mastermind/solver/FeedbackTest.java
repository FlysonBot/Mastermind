package org.mastermind.solver;

import org.junit.jupiter.api.Test;
import org.mastermind.codes.ConvertCode;

import static org.junit.jupiter.api.Assertions.*;

public class FeedbackTest {

    private static final int   COLORS             = 6;  // c parameter
    private static final int   DIGITS             = 4;  // d parameter
    private static final int   TOTAL_COMBINATIONS = 1296; // 6^4
    private static final int[] colorFreqCounter   = new int[10];

    private static int ind(int code) { return ConvertCode.toIndex(COLORS, DIGITS, code); }

    private int getFeedbackQuick(int guessInd, int secretInd) {
        return Feedback.getFeedback(guessInd, secretInd, COLORS, DIGITS, colorFreqCounter);
    }

    @Test
    public void testIterationPerformance() {
        System.out.println("\n=== Iteration Performance Test ===");
        long startTime;
        int  totalCalls = 0;

        startTime = System.nanoTime();

        // Run multiple times
        for (int t = 0; t < 50; t++) {
            // Call getFeedback for all (guess, secret) index pairs
            for (int guessIdx = 0; guessIdx < TOTAL_COMBINATIONS; guessIdx++) {
                for (int secretIdx = 0; secretIdx < TOTAL_COMBINATIONS; secretIdx++) {
                    getFeedbackQuick(guessIdx, secretIdx);
                    totalCalls++;
                }
            }
        }

        long endTime  = System.nanoTime();
        long duration = (endTime - startTime) / 1_000_000;

        System.out.println("Total combinations processed: " + totalCalls);
        System.out.println("Time taken: " + duration + " ms");
        System.out.println("Average per call: " + String.format("%.6f", duration / (double) totalCalls) + " ms");
    }

    @Test
    public void testSingleCombinationPerformance() {
        System.out.println("\n=== Fixed Input Performance Test ===");
        long startTime = System.nanoTime();

        // Run multiple times
        int limit = (int) Math.pow(6, 4);
        for (int t = 0; t < limit; t++) {
            getFeedbackQuick(ind(1123), ind(3456));
        }

        long endTime  = System.nanoTime();
        long duration = (endTime - startTime) / 1_000_000;

        System.out.println("Total combinations processed: " + limit);
        System.out.println("Time taken: " + duration + " ms");
        System.out.println("Average per call: " + String.format("%.6f", duration / (double) limit) + " ms");
    }

    @Test
    public void testEdgeCases() {
        System.out.println("\n=== Edge Cases Test ===");

        // Perfect match
        int result1 = getFeedbackQuick(ind(1111), ind(1111));
        assertEquals(4, result1 / 10, "Perfect match should have 4 blacks");
        assertEquals(0, result1 % 10, "Perfect match should have 0 whites");
        System.out.println("✓ Perfect match (1111 vs 1111): " + result1 / 10 + " black, " + result1 % 10 + " white");

        // No match
        int result2 = getFeedbackQuick(ind(1111), ind(2222));
        assertEquals(0, result2 / 10, "No match should have 0 blacks");
        assertEquals(0, result2 % 10, "No match should have 0 whites");
        System.out.println("✓ No match (1111 vs 2222): " + result2 / 10 + " black, " + result2 % 10 + " white");

        // All whites
        int result3 = getFeedbackQuick(ind(1234), ind(4321));
        assertEquals(0, result3 / 10, "All whites case should have 0 blacks");
        assertEquals(4, result3 % 10, "All whites case should have 4 whites");
        System.out.println("✓ All whites (1234 vs 4321): " + result3 / 10 + " black, " + result3 % 10 + " white");

        // Mixed
        int result4 = getFeedbackQuick(ind(5566), ind(5655));
        assertEquals(1, result4 / 10, "Mixed case blacks");
        assertEquals(2, result4 % 10, "Mixed case whites");
        System.out.println("✓ Mixed (5566 vs 5655): " + result4 / 10 + " black, " + result4 % 10 + " white");
    }

    @Test
    void testGetFeedbackIncrementalMatchesGetFeedback() {
        // For every guess in the 6x4 space, iterate all secrets sequentially using
        // getFeedbackIncremental and verify each result matches getFeedback.
        int   c            = COLORS, d = DIGITS, total = TOTAL_COMBINATIONS;
        int[] colorFreqRef = new int[c];
        int[] result       = new int[3];

        for (int guessInd = 0; guessInd < total; guessInd++) {
            // Pre-extract guess digits
            int[] guessDigits = new int[d];
            int   tmp         = guessInd;
            for (int p = 0; p < d; p++) {
                guessDigits[p] = tmp % c;
                tmp /= c;
            }

            // Bootstrap incremental state at secretInd=0
            int[] colorFreqCounter = new int[c];
            int   feedback0        = Feedback.getFeedback(guessInd, 0, c, d, colorFreqCounter);
            int   black0           = 0;
            int[] secretDigits     = new int[d];
            for (int p = 0; p < d; p++) {
                int gs = guessDigits[p], ss = 0;
                secretDigits[p] = ss;
                if (gs == ss) black0++;
                else {
                    colorFreqCounter[gs]++;
                    colorFreqCounter[ss]--;
                }
            }
            assertEquals(Feedback.getFeedback(guessInd, 0, c, d, colorFreqRef), feedback0,
                         "Bootstrap mismatch at guessInd=" + guessInd + " secretInd=0");

            int colorFreqTotal = 0;
            for (int i = 0; i < c; i++) {
                int f = colorFreqCounter[i];
                colorFreqTotal += f > 0 ? f : -f;
            }

            int black = black0;
            for (int secretInd = 1; secretInd < total; secretInd++) {
                FeedbackIncremental.getFeedbackIncremental(guessDigits, secretDigits, black, colorFreqCounter,
                                                           colorFreqTotal, c,
                                                           d, result);
                black = result[1];
                colorFreqTotal = result[2];
                int expected = Feedback.getFeedback(guessInd, secretInd, c, d, colorFreqRef);
                assertEquals(expected, result[0],
                             "Mismatch at guessInd=" + guessInd + " secretInd=" + secretInd);
            }
        }
    }

    @Test
    void testCalcFeedbackSize() {
        assertEquals(55, Feedback.calcFeedbackSize(9));
    }

    @Test
    void testEnumerateFeedback() {
        int   d         = 9;
        int[] feedbacks = Feedback.enumerateFeedback(d);

        int[] expected = {
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9,          // black = 0, white = 0..9  (10 values)
                10, 11, 12, 13, 14, 15, 16, 17, 18,    // black = 1, white = 0..8  (9 values)
                20, 21, 22, 23, 24, 25, 26, 27,        // black = 2, white = 0..7  (8 values)
                30, 31, 32, 33, 34, 35, 36,            // black = 3, white = 0..6  (7 values)
                40, 41, 42, 43, 44, 45,                // black = 4, white = 0..5  (6 values)
                50, 51, 52, 53, 54,                    // black = 5, white = 0..4  (5 values)
                60, 61, 62, 63,                        // black = 6, white = 0..3  (4 values)
                70, 71, 72,                            // black = 7, white = 0..2  (3 values)
                80, 81,                                // black = 8, white = 0..1  (2 values)
                90                                     // black = 9, white = 0..0  (1 value)
        };

        assertEquals(55, feedbacks.length, "Size should be 55 for d=9");
        assertArrayEquals(expected, feedbacks, "Enumerated feedbacks for d=9 do not match expected values");
    }

}
