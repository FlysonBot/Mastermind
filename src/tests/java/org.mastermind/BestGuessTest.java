package org.mastermind;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BestGuessTest {

    private int[] allCodes;
    private final int d = 4;
    private static final int EXPECTED_BEST_GUESS = 1123;

    /**
     * Setup method that runs before each test.
     * Generates all valid codes (6 pegs, 4 colors) - same as benchmark.
     */
    @BeforeEach
    public void setUp() {
        allCodes = AllValidCode.generateAllCodes(6, 4);
    }

    /**
     * Test the ordinary (sequential) version of findBestGuess.
     * Uses the full code space (all combinations) with parallel = false.
     * Verifies that the result matches the expected best guess of 1123.
     */
    @Test
    public void testOrdinaryVersion() {
        // Act: Call the ordinary version with parallel = false
        int bestGuess = (int) BestGuess.findBestGuess(allCodes, allCodes, d, false)[0];

        // Assert: Verify the result matches the expected value
        assertEquals(EXPECTED_BEST_GUESS, bestGuess);
    }

    /**
     * Test the parallel version of findBestGuess.
     * Uses the full code space (all combinations) with parallel = true.
     * Verifies that the result matches the expected best guess of 1123.
     */
    @Test
    public void testParallelVersion() {
        // Act: Call the parallel version with parallel = true
        int bestGuess = (int) BestGuess.findBestGuess(allCodes, allCodes, d, true)[0];

        // Assert: Verify the result matches the expected value
        assertEquals(EXPECTED_BEST_GUESS, bestGuess);

        BestGuess.shutdown();
    }
}
