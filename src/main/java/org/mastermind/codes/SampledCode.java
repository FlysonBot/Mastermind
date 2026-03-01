package org.mastermind.codes;

import java.util.Random;

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
     * Generate a random Monte Carlo sample from all possible Mastermind code
     * with the specified sample size.
     *
     * @param c          number of colors (<= 9)
     * @param d          number of digits (<= 9)
     * @param sampleSize size of the sample
     * @return A random sample of all possible Mastermind code
     */
    public static int[] getSample(int c, int d, int sampleSize) {
        Random random = new Random();
        int[]  sample = new int[sampleSize];

        for (int i = 0; i < sampleSize; i++) {
            int code = 0;
            for (int digit = 0; digit < d; digit++) {
                int color = random.nextInt(c) + 1; // colors 1..c
                code = code * 10 + color;
            }
            sample[i] = code;
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
     * Calculates the required sample size with a default tolerance of 0.05 (5%).
     *
     * @param feedbackSize Number of possible feedback values K (e.g., 55)
     * @return The required number of random secrets to sample.
     * @see #calcSampleSizeForSecrets(int, double)
     */
    public static int calcSampleSizeForSecrets(int feedbackSize) {
        return calcSampleSizeForSecrets(feedbackSize, 0.01);
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
