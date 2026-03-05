package org.mastermind.codes;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.util.BitSet;

import static org.junit.jupiter.api.Assertions.*;

class SampledCodeTest {

    @Test
    void testReturnsSampleOfCorrectSize() {
        int[] result = SampledCode.getSample(6, 4, 1000);
        assertEquals(1000, result.length);
    }

    @Test
    void testSampleSizeZeroReturnsEmptyArray() {
        int[] result = SampledCode.getSample(6, 4, 0);
        assertNotNull(result);
        assertEquals(0, result.length);
    }

    @ParameterizedTest
    @CsvSource({ "6,4", "3,3", "8,5", "2,1" })
    void testAllIndicesWithinRange(int c, int d) {
        int   total  = (int) Math.pow(c, d);
        int[] result = SampledCode.getSample(c, d, 1000);
        for (int ind : result) {
            assertTrue(ind >= 0 && ind < total,
                       "Index " + ind + " out of range [0," + total + ")");
        }
    }

    @Test
    void testResultIsActuallyRandom() {
        // With 1000 samples from 6^4=1296 possible indices, we expect reasonable variety.
        // The chance of getting fewer than 100 unique values is astronomically small.
        int[] result      = SampledCode.getSample(6, 4, 1000);
        long  uniqueCount = java.util.Arrays.stream(result).distinct().count();
        assertTrue(uniqueCount > 100,
                   "Expected high variety in samples, got only " + uniqueCount + " unique indices");
    }

    // --- getValidSample ---

    @Test
    void testGetValidSampleEnumerationPathOnlyReturnsSetBits() {
        // validCount <= MAX_ENUM: enumeration path
        BitSet remaining = new BitSet(10);
        remaining.set(1);
        remaining.set(3);
        remaining.set(7);
        int[] result = SampledCode.getValidSample(remaining, 3, 2, 4, 50);
        for (int idx : result) {
            assertTrue(remaining.get(idx), "Index " + idx + " is not a set bit");
        }
    }

    @Test
    void testGetValidSampleRejectionPathOnlyReturnsSetBits() {
        // validCount > MAX_ENUM: rejection sampling path.
        // We fake this by constructing a BitSet where all bits are set and validCount > MAX_ENUM.
        int    total     = SampledCode.MAX_ENUM + 1;
        BitSet remaining = new BitSet(total);
        remaining.set(0, total); // all bits set so rejection always succeeds immediately
        int[] result = SampledCode.getValidSample(remaining, total, 9, 7, 50);
        for (int idx : result) {
            assertTrue(idx >= 0 && idx < total, "Index " + idx + " out of range");
            assertTrue(remaining.get(idx), "Index " + idx + " is not a set bit");
        }
    }

    @Test
    void testGetValidSampleWithSampleSizeExceedingValidCount() {
        // Sampling with replacement: duplicates are expected, should not throw
        BitSet remaining = new BitSet(10);
        remaining.set(2);
        remaining.set(5);
        int[] result = SampledCode.getValidSample(remaining, 2, 2, 4, 100);
        assertEquals(100, result.length);
        for (int idx : result) {
            assertTrue(remaining.get(idx), "Index " + idx + " is not a set bit");
        }
    }
}
