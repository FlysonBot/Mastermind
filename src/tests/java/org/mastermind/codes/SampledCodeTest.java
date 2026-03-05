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

    // --- calcSampleSizeForSecrets accuracy ---

    @Test
    void testCalcSampleSizeForSecretsInflationWithinTolerance() {
        // Setup: K=10 feedback buckets, true probabilities p_i = 1/K (uniform distribution).
        // True S = Σ p_i^2 = K * (1/K)^2 = 1/K.
        // The formula guarantees E[Ŝ] - S <= tolerance * S on average.
        // We verify the mean estimated S across many trials stays within tolerance of true S.
        int    K         = 10;
        double tolerance = 0.05;
        int    N         = SampledCode.calcSampleSizeForSecrets(K, tolerance);
        double trueS     = 1.0 / K;

        // Each trial: draw N samples from K categories uniformly, compute Ŝ = Σ (count_i/N)^2
        int    trials       = 2000;
        double sumInflation = 0;
        int[]  counts       = new int[K];
        int[]  sample       = new int[N];
        for (int t = 0; t < trials; t++) {
            java.util.Arrays.fill(counts, 0);
            for (int i = 0; i < N; i++) {
                sample[i] = java.util.concurrent.ThreadLocalRandom.current().nextInt(K);
            }
            for (int s : sample) counts[s]++;
            double sHat = 0;
            for (int cnt : counts) {
                double p = (double) cnt / N;
                sHat += p * p;
            }
            sumInflation += (sHat - trueS) / trueS;
        }
        double meanInflation = sumInflation / trials;
        // The formula targets mean inflation ≈ tolerance (it's an upper bound, not strict <).
        // Allow 10% slack above tolerance to absorb Monte Carlo variance across 2000 trials.
        assertTrue(meanInflation <= tolerance * 1.1,
                   "Mean relative inflation " + meanInflation + " exceeded tolerance " + tolerance);
    }

    // --- calcSampleSizeForGuesses confidence ---

    @Test
    void testCalcSampleSizeForGuessesHitsTopPercentileWithExpectedConfidence() {
        // Setup: population of 1000 guesses; top x% = top 10 guesses (1%).
        // Sample n = calcSampleSizeForGuesses(0.01, 0.99) guesses.
        // In >= 99% of trials, at least one sampled guess should be in the top 1%.
        double percentile = 0.01;
        double confidence = 0.99;
        int    n          = SampledCode.calcSampleSizeForGuesses(percentile, confidence);
        int    population = 1000;
        int    topK       = (int) (population * percentile); // 10

        int trials  = 5000;
        int success = 0;
        for (int t = 0; t < trials; t++) {
            boolean found = false;
            for (int i = 0; i < n && !found; i++) {
                // A sampled guess index is "elite" if it falls in [0, topK)
                int idx = java.util.concurrent.ThreadLocalRandom.current().nextInt(population);
                if (idx < topK) found = true;
            }
            if (found) success++;
        }

        double observedConfidence = (double) success / trials;
        // Allow a small margin below the stated confidence for statistical variation
        assertTrue(observedConfidence >= confidence - 0.02,
                   "Observed confidence " + observedConfidence + " below expected " + confidence);
    }
}
