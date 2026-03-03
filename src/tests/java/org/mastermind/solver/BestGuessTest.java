package org.mastermind.solver;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mastermind.codes.ConvertCode;

import static org.junit.jupiter.api.Assertions.*;

public class BestGuessTest {

    private static final int   C = 6;
    private static final int   D = 4;
    private              int[] allInd;

    private static int ind(int code) { return ConvertCode.toIndex(C, D, code); }

    @BeforeEach
    public void setUp() {
        allInd = new int[(int) Math.pow(C, D)];
        for (int i = 0; i < allInd.length; i++) allInd[i] = i;
    }

    /**
     * Test the ordinary (sequential) version of findBestGuess.
     * Uses the full code space (all combinations) with parallel = false.
     * Verifies that the result matches the expected best guess of 1123.
     */
    @Test
    public void testOrdinaryVersion() {
        int bestGuessInd = (int) BestGuess.findBestGuess(allInd, allInd, C, D, false)[0];
        assertEquals(ind(1123), bestGuessInd);
    }

    /**
     * Test the parallel version of findBestGuess.
     * Uses the full code space (all combinations) with parallel = true.
     * Verifies that the result matches the expected best guess of 1123.
     */
    @Test
    public void testParallelVersion() {
        int bestGuessInd = (int) BestGuess.findBestGuess(allInd, allInd, C, D, true)[0];
        assertEquals(ind(1123), bestGuessInd);

        BestGuess.shutdown();
    }
}
