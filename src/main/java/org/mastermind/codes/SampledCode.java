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
     * Estimate the sample size needed for an accurate Monte Carlo sample
     * for the purpose of estimating the distribution of feedback values
     * for a guess.
     *
     * @param feedbackSize number of possible feedback values in the game
     * @return Conservative estimation of the sample size
     */
    public static int calcSampleSize(int feedbackSize) { return (int) (feedbackSize * Math.pow(1.96 / 0.05, 2)); }
}
