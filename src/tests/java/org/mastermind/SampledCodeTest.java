package org.mastermind;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.*;

class SampledCodeTest {

    @Test
    void testReturnsSampleOfCorrectSize() {
        int[] result = SampledCode.getSample(6, 4, 1000);
        assertEquals(1000, result.length);
    }

    @Test
    void testAllCodesHaveCorrectNumberOfDigits() {
        int d = 4;
        int[] result = SampledCode.getSample(6, d, 1000);
        for (int code : result) {
            int digitCount = String.valueOf(code).length();
            assertEquals(d, digitCount, "Code " + code + " does not have " + d + " digits");
        }
    }

    @ParameterizedTest
    @CsvSource({"6,4", "3,3", "8,5", "2,1"})
    void testAllDigitsWithinColorRange(int c, int d) {
        int[] result = SampledCode.getSample(c, d, 1000);
        for (int code : result) {
            String s = String.valueOf(code);
            for (char ch : s.toCharArray()) {
                int digit = ch - '0';
                assertTrue(digit >= 1 && digit <= c,
                        "Digit " + digit + " out of range [1," + c + "] in code " + code);
            }
        }
    }

    @Test
    void testSampleSizeZeroReturnsEmptyArray() {
        int[] result = SampledCode.getSample(6, 4, 0);
        assertNotNull(result);
        assertEquals(0, result.length);
    }

    @Test
    void testSinglePeg() {
        int c = 6, d = 1;
        int[] result = SampledCode.getSample(c, d, 500);
        for (int code : result) {
            assertTrue(code >= 1 && code <= c,
                    "Single-peg code " + code + " out of range [1," + c + "]");
        }
    }

    @Test
    void testResultIsActuallyRandom() {
        // With 1000 samples from 6^4=1296 possible codes, we expect reasonable variety.
        // The chance of getting fewer than 100 unique values is astronomically small.
        int[] result = SampledCode.getSample(6, 4, 1000);
        long uniqueCount = java.util.Arrays.stream(result).distinct().count();
        assertTrue(uniqueCount > 100,
                "Expected high variety in samples, got only " + uniqueCount + " unique codes");
    }

    @Test
    void testOnlyOneColor() {
        // With c=1, every code must be all 1s, e.g. 1111 for d=4
        int d = 4;
        int[] result = SampledCode.getSample(1, d, 100);
        for (int code : result) {
            assertEquals(1111, code, "With c=1 and d=4, every code must be 1111");
        }
    }
}