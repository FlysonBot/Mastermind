package org.mastermind.compute;

/**
 * In Mastermind, after each guess, the solution space is reduced
 * to the set of secrets whose feedback value with the guess matches
 * the observed feedback value. Therefore, the expected average
 * size of the solution space can be calculated by summing for each
 * secret, how many secrets has the same feedback, and divide by the
 * total. This can be simplified to summing the frequency squared
 * then divide by total. This expected size is a key metric to
 * determine the best guess in the MiniAverage approach by picking a
 * guess that produce the minimum expected size. However, since the
 * exact value doesn't matter to the algorithm and only the relative
 * ranking does, it is possible to simplify the calculation to just
 * return the sum of frequency square without any division.
 */
public class ExpectedSize {
    private final int[] validFeedback;

    public ExpectedSize(int d) {
        validFeedback = Feedback.enumerateFeedback(d);
    }

    /**
     * Calculate the sum of number of remaining solution for each secret.
     * <p>
     * This is part of the formula for calculating the average solution size (aka
     * expected size). It is the number obtained before dividing by total. Avoiding
     * division in this function save time for algorithm that only relies on rank
     * and not necessary the exact expected value.
     * </p>
     *
     * @param guessInd     index of the guess code (0-based, base-c encoding)
     * @param secretsInd   list of secret indices (0-based, base-c encoding)
     * @param c            number of colors (<= 9)
     * @param d            number of digits (<= 9)
     * @param feedbackFreq int array of 0 with length 100
     * @return Sum of number of remaining solution for each secret
     */
    public long calcExpectedRank(int guessInd, int[] secretsInd, int c, int d, int[] feedbackFreq) {

        // Calculate feedback for each secret
        int[] colorFreqCounter = new int[c];
        for (int secretInd : secretsInd) {
            int feedback = Feedback.getFeedback(guessInd, secretInd, c, d, colorFreqCounter);
            feedbackFreq[feedback]++;
        }

        // Find the sum of square
        long sum = 0;
        long freq;
        for (int feedback : validFeedback) {
            freq = feedbackFreq[feedback];
            sum += freq * freq;
            feedbackFreq[feedback] = 0;
        }

        return sum;
    }

    /**
     * Convert a rank to the true expected size.
     *
     * @param rank  value returned by {@link #calcExpectedRank}
     * @param total total number of secrets (size of the solution space)
     * @return expected solution space size after the guess
     */
    public float convertRankToExpectedSize(long rank, int total) {
        return (float) rank / total;
    }

    /**
     * Convert a sample-based rank to an estimated expected size for the full population.
     *
     * @param rank           value returned by {@link #calcExpectedRank} computed on the sample
     * @param sampleSize     number of secrets in the sample
     * @param populationSize total number of secrets in the full solution space
     * @return estimated expected solution space size after the guess
     */
    public float convertSampleRankToExpectedSize(long rank, int sampleSize, int populationSize) {
        return (float) rank * (float) populationSize / (float) Math.pow(sampleSize, 2);
    }

    /**
     * Calculate the expected solution space size directly (rank divided by total).
     *
     * @param guessInd     index of the guess code (0-based, base-c encoding)
     * @param secretsInd   list of secret indices (0-based, base-c encoding)
     * @param c            number of colors (<= 9)
     * @param d            number of digits (<= 9)
     * @param feedbackFreq int array of 0 with length 100
     * @return expected solution space size after the guess
     */
    public float calcExpectedSize(int guessInd, int[] secretsInd, int c, int d, int[] feedbackFreq) {
        return convertRankToExpectedSize(calcExpectedRank(guessInd, secretsInd, c, d, feedbackFreq), secretsInd.length);
    }

    /**
     * Incremental variant of {@link #calcExpectedRank} for the full secret space (0..c^d-1).
     * Instead of an arbitrary secrets array, iterates all indices sequentially and uses
     * {@link FeedbackIncremental} to avoid recomputing digit decompositions from scratch.
     *
     * @param guessInd     index of the guess code (0-based, base-c encoding)
     * @param c            number of colors (<= 9)
     * @param d            number of digits (<= 9)
     * @param total        c^d (total number of codes)
     * @param feedbackFreq int array of 0 with length 100
     * @return Sum of squared feedback frequencies (same semantics as {@link #calcExpectedRank})
     */
    public long calcExpectedRankFirst(int guessInd, int c, int d, int total, int[] feedbackFreq) {
        // Set up incremental feedback state
        FeedbackIncremental.State init             = FeedbackIncremental.setupIncremental(guessInd, 0, c, d);
        int[]                     guessDigits      = init.guessDigits();
        int[]                     secretDigits     = init.secretDigits();
        int[]                     colorFreqCounter = init.colorFreqCounter();
        int                       black            = init.black();
        int                       colorFreqTotal   = init.colorFreqTotal();

        // Handle secret index 0 (setup already computed its feedback)
        feedbackFreq[black * 9 + d - (colorFreqTotal >>> 1)]++;

        // Iterate remaining secrets incrementally, updating secretDigits and feedback state in place
        int[] result = new int[3];
        for (int secretInd = 1; secretInd < total; secretInd++) {
            FeedbackIncremental.getFeedbackIncremental(guessDigits, secretDigits, black, colorFreqCounter,
                                                       colorFreqTotal, c, d, result);
            black = result[1];
            colorFreqTotal = result[2];
            feedbackFreq[result[0]]++;
        }

        // Sum squared frequencies and reset feedbackFreq for reuse
        long sum = 0;
        long freq;
        for (int feedback : validFeedback) {
            freq = feedbackFreq[feedback];
            sum += freq * freq;
            feedbackFreq[feedback] = 0;
        }

        return sum;
    }
}
