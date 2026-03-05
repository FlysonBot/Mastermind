package org.mastermind.solver;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class BestFirstGuessTest {

    @Test
    public void allValidGamesReturnNonNullResult() {
        for (int c = 2; c <= 9; c++) {
            for (int d = 1; d <= 9; d++) {
                long[] result = BestFirstGuess.of(c, d);
                assertNotNull(result, "Expected result for c=" + c + ", d=" + d);
                assertEquals(2, result.length, "Expected length 2 for c=" + c + ", d=" + d);
                assertTrue(result[0] > 0, "Expected positive guess code for c=" + c + ", d=" + d);
                assertTrue(result[1] > 0, "Expected positive rank for c=" + c + ", d=" + d);
            }
        }
    }

    @Test
    public void invalidColorsThrowException() {
        assertThrows(IllegalArgumentException.class, () -> BestFirstGuess.of(1, 4));
        assertThrows(IllegalArgumentException.class, () -> BestFirstGuess.of(10, 4));
        assertThrows(IllegalArgumentException.class, () -> BestFirstGuess.of(0, 4));
    }

    @Test
    public void invalidDigitsThrowException() {
        assertThrows(IllegalArgumentException.class, () -> BestFirstGuess.of(4, 0));
        assertThrows(IllegalArgumentException.class, () -> BestFirstGuess.of(4, 10));
    }
}
