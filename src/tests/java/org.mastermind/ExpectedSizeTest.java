package org.mastermind;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ExpectedSizeTest {

    private static final int COLORS = 6;
    private static final int DIGITS = 4;
    private static final float DELTA = 0.001f;
    private static final int[] feedbackFreq = new int[100];
    private static final ExpectedSize expectedSizeObj = new ExpectedSize(DIGITS);
    int[] secrets = AllValidCode.generateAllCodes(COLORS, DIGITS);
    
    private float calcExpectedSize(int guess, int[] secrets) {
        return expectedSizeObj.calcExpectedSize(guess, secrets, DIGITS, feedbackFreq);
    }

    @Test
    public void testExpectedSize() {
        assertEquals(204.5355f, calcExpectedSize(1122, secrets), DELTA);
        assertEquals(185.2685f, calcExpectedSize(1123, secrets), DELTA);
        assertEquals(188.1898f, calcExpectedSize(1234, secrets), DELTA);
        assertEquals(235.9491f, calcExpectedSize(1112, secrets), DELTA);
        assertEquals(511.9799f, calcExpectedSize(1111, secrets), DELTA);
        assertEquals(204.5355f, calcExpectedSize(1212, secrets), DELTA);
    }

    @Test
    public void testExpectedSizeSymmetry() {
        // Guesses with the same color multiset should yield the same expected size
        float base = calcExpectedSize(1122, secrets);
        assertEquals(base, calcExpectedSize(1212, secrets), DELTA);
        assertEquals(base, calcExpectedSize(2211, secrets), DELTA);
        assertEquals(base, calcExpectedSize(2121, secrets), DELTA);
    }
}