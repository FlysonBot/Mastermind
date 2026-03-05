package org.mastermind.codes;

import java.util.BitSet;
import java.util.concurrent.ThreadLocalRandom;

/**
 * The Monte Carlo method is a way to estimate population parameters
 * by calculating the statistics on a sample. In the context of
 * Mastermind, the feedback distribution needed to calculate the
 * expected remaining valid solutions can be estimated with a
 * sample of secrets instead of iterating through all possible
 * secrets, allowing for faster computation for larger game.
 */
public class SampledCode {

    /**
     * Maximum validCount for which enumeration is used. Above this threshold,
     * int[validCount] becomes too large (>20MB) and rejection sampling is used instead.
     * At this threshold, fill rate is always high enough that rejection is fast.
     * Empirically derived from timing tests across c=7-9, d=7-9 game sizes.
     */
    static final int MAX_ENUM = 5_000_000;

    /**
     * Generate a random Monte Carlo sample of code indices from all possible
     * Mastermind codes with the specified sample size.
     *
     * @param c          number of colors (<= 9)
     * @param d          number of digits (<= 9)
     * @param sampleSize size of the sample
     * @return A random sample of code indices in [0, c^d)
     */
    public static int[] getSample(int c, int d, int sampleSize) {
        int   total  = (int) Math.pow(c, d);
        int[] sample = new int[sampleSize];

        for (int i = 0; i < sampleSize; i++) {
            sample[i] = ThreadLocalRandom.current().nextInt(total);
        }

        return sample;
    }

    /**
     * Generate a random Monte Carlo sample of code indices from the current valid secrets.
     *
     * @param remaining  BitSet of valid secret indices
     * @param validCount number of set bits in {@code remaining}
     * @param c          number of colors (<= 9)
     * @param d          number of digits (<= 9)
     * @param sampleSize size of the sample
     * @return A random sample of valid code indices
     */
    public static int[] getValidSample(BitSet remaining, int validCount, int c, int d, int sampleSize) {
        int   total  = (int) Math.pow(c, d);
        int[] sample = new int[sampleSize];

        if (validCount <= MAX_ENUM) {
            // Enumeration: bounded memory (≤20MB), fast scan, fast random access.
            int[] valid = new int[validCount];
            int   j     = 0;
            for (int i = remaining.nextSetBit(0); i >= 0; i = remaining.nextSetBit(i + 1)) {
                valid[j++] = i;
            }
            for (int i = 0; i < sampleSize; i++) {
                sample[i] = valid[ThreadLocalRandom.current().nextInt(validCount)];
            }
        } else {
            // Rejection sampling: validCount is large so fill rate is high and rejection is fast.
            for (int i = 0; i < sampleSize; i++) {
                int idx;
                do { idx = ThreadLocalRandom.current().nextInt(total); } while (!remaining.get(idx));
                sample[i] = idx;
            }
        }

        return sample;
    }

    /**
     * Calculates the required sample size for the secret space using a
     * Bias-to-Signal Ratio approach.
     * <p>
     * In Mastermind, we estimate the "Expected Remaining Solutions" (S = Σ p_i^2),
     * where p_i is the probability of feedback category i. When estimating S from
     * a random sample, the estimate will be higher than the true value:
     * E(Ŝ) = S + (1 - S) / N. This inflation comes from sampling variance in
     * the squared probabilities.
     * <p>
     * To ensure the sampling inflation (1 - S) / N doesn't exceed a tolerance
     * percentage of the true signal S, we require: (1 - S) / N ≤ tolerance × S.
     * Solving for N gives: N ≥ (1 - S) / (tolerance × S).
     * <p>
     * Since S varies by guess quality (ranging from 1/K at worst to 1 at best),
     * we use the worst-case bound: N ≥ (K - 1) / tolerance. This single value
     * of N protects all possible guesses from sampling inflation.
     * <p>
     * Note: This is a conservative overestimation for the sample size, but still
     * manageable for bruteforce. For d=9, K=55, tolerance = 0.01, sample size
     * is about 5400, which is very manageable while still being conservative.
     *
     * @param feedbackSize Number of possible feedback values K (e.g., 55)
     * @param tolerance    Maximum acceptable inflation as a fraction of S (e.g., 0.05)
     * @return The required number of random secrets to sample.
     */
    public static int calcSampleSizeForSecrets(int feedbackSize, double tolerance) {
        return (int) Math.ceil((feedbackSize - 1) / tolerance);
    }

    /**
     * Calculate the sample size for guesses needed to ensure that
     * the probability of including at least one "elite" guess in the top x%
     * is (1 - δ) confident.
     * <p>
     * Uses the formula: n ≥ ln(δ) / ln(1 - x)
     * <p>
     * For example, it only takes a sample of 6905 guesses in order to find
     * the top 0.1% of guesses with 99.9% confidence.
     *
     * @param percentileThreshold the percentile threshold x as a decimal
     *                            (e.g., 0.01 for top 1%)
     * @param confidence          the confidence level (e.g., 0.99 for 99% sure)
     * @return The required sample size for guesses
     */
    public static int calcSampleSizeForGuesses(double percentileThreshold, double confidence) {
        return (int) Math.ceil(Math.log(1.0 - confidence) / Math.log(1.0 - percentileThreshold));
    }

}
