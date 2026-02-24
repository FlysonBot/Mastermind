package org.mastermind;

public class ExpectedSize {
    private final int[] validFeedback;

    public ExpectedSize(int d) {
        validFeedback = Feedback.enumerateFeedback(d);
    }

    /**
     * Calculate sum of square of the number of remaining solution after a guess.
     * <p>
     * This is part of the formula for calculating the average solution size (aka
     * expected size). It is the number obtained before dividing by total. Avoiding
     * division in this function save time for algorithm that only relies on rank
     * and not necessary the true expected value.
     * </p>
     *
     * @param guess         code, digits 1..c, length d
     * @param secrets       list of codes, digits 1..c, length d
     * @param d             number of digits (<= 9)
     * @param feedbackFreq  int array of 0 with length c
     */
    public int calcExpectedRank(int guess, int[] secrets, int d, int[] feedbackFreq) {

        // Calculate feedback for each secret
        int[] colorFreqCounter = new int[10];
        for (int secret: secrets) {
            int feedback = Feedback.getFeedback(guess, secret, d, colorFreqCounter);
            feedbackFreq[feedback]++;
        }

        // Find the sum of square
        int sum = 0;
        int freq;
        for (int feedback: validFeedback) {
            freq = feedbackFreq[feedback];
            sum += freq * freq;
            feedbackFreq[feedback] = 0;
        }

        return sum;
    }

    public float calcExpectedSize(int guess, int[] secrets, int d, int total, int[] feedbackFreq) {
        return (float) calcExpectedRank(guess, secrets, d, feedbackFreq) / total;
    }

    public float calcExpectedProportion(int guess, int[] secrets, int d, int total, int[] feedbackFreq) {
        return (float) calcExpectedRank(guess, secrets, d, feedbackFreq) / (float) Math.pow(total, 3);
    }
}
