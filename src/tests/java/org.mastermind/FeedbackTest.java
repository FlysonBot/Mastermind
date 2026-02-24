package org.mastermind;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class FeedbackTest {

    private static final int COLORS = 6;  // c parameter
    private static final int DIGITS = 4;  // d parameter
    private static final int TOTAL_COMBINATIONS = 1296; // 6^4
    private static final int[] colorFreqCounter = new int[10];

    /**
     * Converts a combination index to its Mastermind representation.
     * For example, with 6 colors and 4 digits:
     * 0 -> 1111, 1 -> 1112, 2 -> 1113, ..., 5 -> 1116, 6 -> 1121, etc.
     */
    private int indexToCombination(int index) {
        int result = 0;
        int divisor = 1;

        for (int i = 0; i < DIGITS; i++) {
            int digit = (index % COLORS) + 1;
            result += digit * divisor;
            divisor *= 10;
            index /= COLORS;
        }

        return result;
    }

    private int getFeedbackQuick(int guess, int secret) {
        return Feedback.getFeedback(guess, secret, DIGITS, colorFreqCounter);
    }

    @Test
    public void testIterationPerformance() {
        System.out.println("\n=== Iteration Performance Test ===");
        long startTime;
        int totalCalls = 0;

        // Pre-generate all combinations OUTSIDE the timer
        int[] allCombinations = new int[TOTAL_COMBINATIONS];
        for (int i = 0; i < TOTAL_COMBINATIONS; i++) {
            allCombinations[i] = indexToCombination(i);
        }

        int[] secrets = new int[TOTAL_COMBINATIONS];
        System.arraycopy(allCombinations, 0, secrets, 0, TOTAL_COMBINATIONS);

        startTime = System.nanoTime();

        // Run multiple times
        for (int t=0; t<100; t++) {
            // Call single version 1,296 times, storing results in a 2D array
            for (int guessIdx = 0; guessIdx < TOTAL_COMBINATIONS; guessIdx++) {
                int guess = allCombinations[guessIdx];

                for (int secretIdx = 0; secretIdx < TOTAL_COMBINATIONS; secretIdx++) {
                    int secret = secrets[secretIdx];
                    getFeedbackQuick(guess, secret);
                    totalCalls++;
                }
            }
        }

        long endTime = System.nanoTime();
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
        for (int t=0; t<limit; t++) {
            getFeedbackQuick(1123, 3456);
        }

        long endTime = System.nanoTime();
        long duration = (endTime - startTime) / 1_000_000;

        System.out.println("Total combinations processed: " + limit);
        System.out.println("Time taken: " + duration + " ms");
        System.out.println("Average per call: " + String.format("%.6f", duration / (double) limit) + " ms");
    }

    @Test
    public void testEdgeCases() {
        System.out.println("\n=== Edge Cases Test ===");

        // Perfect match
        int result1 = getFeedbackQuick(1111, 1111);
        assertEquals(4, result1 / 10, "Perfect match should have 4 blacks");
        assertEquals(0, result1 % 10, "Perfect match should have 0 whites");
        System.out.println("✓ Perfect match (1111 vs 1111): " + result1 / 10 + " black, " + result1 % 10 + " white");

        // No match
        int result2 = getFeedbackQuick(1111, 2222);
        assertEquals(0, result2 / 10, "No match should have 0 blacks");
        assertEquals(0, result2 % 10, "No match should have 0 whites");
        System.out.println("✓ No match (1111 vs 2222): " + result2 / 10 + " black, " + result2 % 10 + " white");

        // All whites
        int result3 = getFeedbackQuick(1234, 4321);
        assertEquals(0, result3 / 10, "All whites case should have 0 blacks");
        assertEquals(4, result3 % 10, "All whites case should have 4 whites");
        System.out.println("✓ All whites (1234 vs 4321): " + result3 / 10 + " black, " + result3 % 10 + " white");

        // Mixed
        int result4 = getFeedbackQuick(5566, 5655);
        assertEquals(1, result4 / 10, "Mixed case blacks");
        assertEquals(2, result4 % 10, "Mixed case whites");
        System.out.println("✓ Mixed (1122 vs 1211): " + result4 / 10 + " black, " + result4 % 10 + " white");
    }

    @Test
    void testCalcFeedbackSize() {
        assertEquals(55, Feedback.calcFeedbackSize(9));
    }

    @Test
    void testEnumerateFeedback() {
        int d = 9;
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
