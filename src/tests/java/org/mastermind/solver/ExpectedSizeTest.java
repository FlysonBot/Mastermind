package org.mastermind.solver;

import org.junit.jupiter.api.Test;
import org.mastermind.codes.ConvertCode;

import static org.junit.jupiter.api.Assertions.*;

public class ExpectedSizeTest {

    private static final int          COLORS          = 6;
    private static final int          DIGITS          = 4;
    private static final int          TOTAL           = 1296; // 6^4
    private static final float        DELTA           = 0.001f;
    private static final int[]        feedbackFreq    = new int[100];
    private static final ExpectedSize expectedSizeObj = new ExpectedSize(DIGITS);

    // All secret indices 0..TOTAL-1
    private static final int[] secretsInd;

    static {
        secretsInd = new int[TOTAL];
        for (int i = 0; i < TOTAL; i++) secretsInd[i] = i;
    }

    private static int ind(int code) { return ConvertCode.toIndex(COLORS, DIGITS, code); }

    private float calcExpectedSize(int guessInd) {
        return expectedSizeObj.calcExpectedSize(guessInd, secretsInd, COLORS, DIGITS, feedbackFreq);
    }

    @Test
    public void testExpectedSize() {
        assertEquals(204.5355f, calcExpectedSize(ind(1122)), DELTA);
        assertEquals(185.2685f, calcExpectedSize(ind(1123)), DELTA);
        assertEquals(188.1898f, calcExpectedSize(ind(1234)), DELTA);
        assertEquals(235.9491f, calcExpectedSize(ind(1112)), DELTA);
        assertEquals(511.9799f, calcExpectedSize(ind(1111)), DELTA);
        assertEquals(204.5355f, calcExpectedSize(ind(1212)), DELTA);
    }

    @Test
    public void testCalcExpectedRankFirstMatchesFullRank() {
        int[] guesses = { ind(1122), ind(1123), ind(1234) };
        for (int guessInd : guesses) {
            long rankFull = expectedSizeObj.calcExpectedRank(guessInd, secretsInd, COLORS, DIGITS, feedbackFreq);
            long rankInc  = expectedSizeObj.calcExpectedRankFirst(guessInd, COLORS, DIGITS, TOTAL, feedbackFreq);
            assertEquals(rankFull, rankInc, "calcExpectedRankFirst mismatch for guess index " + guessInd);
        }
    }

    @Test
    public void testExpectedSizeSymmetry() {
        // Guesses with the same color multiset should yield the same expected size
        float base = calcExpectedSize(ind(1122));
        assertEquals(base, calcExpectedSize(ind(1212)), DELTA);
        assertEquals(base, calcExpectedSize(ind(2211)), DELTA);
        assertEquals(base, calcExpectedSize(ind(2121)), DELTA);
    }
}