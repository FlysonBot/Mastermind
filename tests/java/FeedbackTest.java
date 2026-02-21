import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class FeedbackTest {

    private static final int COLORS = 6;  // c parameter
    private static final int DIGITS = 4;  // d parameter
    private static final int TOTAL_COMBINATIONS = 1296; // 6^4

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

    @Test
    public void testSingleCallPerformance() {
        System.out.println("\n=== Single Call Performance (First Overload) ===");
        long startTime = 0;
        int totalCalls = 0;

        // Pre-generate all combinations OUTSIDE the timer
        int[] allCombinations = new int[TOTAL_COMBINATIONS];
        for (int i = 0; i < TOTAL_COMBINATIONS; i++) {
            allCombinations[i] = indexToCombination(i);
        }

        int[] secrets = new int[TOTAL_COMBINATIONS];
        System.arraycopy(allCombinations, 0, secrets, 0, TOTAL_COMBINATIONS);

        startTime = System.nanoTime();
        totalCalls = 0;

        // Run 40 times
        for (int t=0; t<80; t++) {
            // Call single version 1,296 times, storing results in a 2D array
            for (int guessIdx = 0; guessIdx < TOTAL_COMBINATIONS; guessIdx++) {
                int guess = allCombinations[guessIdx];

                for (int secretIdx = 0; secretIdx < TOTAL_COMBINATIONS; secretIdx++) {
                    int secret = secrets[secretIdx];
                    int[] feedback = Feedback.getFeedback(guess, secret, COLORS, DIGITS);

                    assertNotNull(feedback);
                    assertEquals(2, feedback.length);
                    assertTrue(feedback[0] >= 0 && feedback[0] <= DIGITS,
                            "Black count out of range for guess=" + guess + ", secret=" + secret);
                    assertTrue(feedback[1] >= 0 && feedback[1] <= DIGITS - feedback[0],
                            "White count out of range for guess=" + guess + ", secret=" + secret);
                    assertTrue(feedback[0] + feedback[1] <= DIGITS,
                            "Sum of black and white count out of range for guess=" + guess + ", secret=" + secret);

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
    public void testEdgeCases() {
        System.out.println("\n=== Edge Cases Test ===");

        // Perfect match
        int[] result1 = Feedback.getFeedback(1111, 1111, COLORS, DIGITS);
        assertEquals(4, result1[0], "Perfect match should have 4 blacks");
        assertEquals(0, result1[1], "Perfect match should have 0 whites");
        System.out.println("✓ Perfect match (1111 vs 1111): " + result1[0] + " black, " + result1[1] + " white");

        // No match
        int[] result2 = Feedback.getFeedback(1111, 2222, COLORS, DIGITS);
        assertEquals(0, result2[0], "No match should have 0 blacks");
        assertEquals(0, result2[1], "No match should have 0 whites");
        System.out.println("✓ No match (1111 vs 2222): " + result2[0] + " black, " + result2[1] + " white");

        // All whites
        int[] result3 = Feedback.getFeedback(1234, 4321, COLORS, DIGITS);
        assertEquals(0, result3[0], "All whites case should have 0 blacks");
        assertEquals(4, result3[1], "All whites case should have 4 whites");
        System.out.println("✓ All whites (1234 vs 4321): " + result3[0] + " black, " + result3[1] + " white");

        // Mixed
        int[] result4 = Feedback.getFeedback(1122, 1211, COLORS, DIGITS);
        assertEquals(1, result4[0], "Mixed case blacks");
        assertEquals(2, result4[1], "Mixed case whites");
        System.out.println("✓ Mixed (1122 vs 1211): " + result4[0] + " black, " + result4[1] + " white");
    }
}
