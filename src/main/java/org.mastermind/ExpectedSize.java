package org.mastermind;

public class ExpectedSize {
    private final int[] validFeedback;

    public ExpectedSize(int d) {
        validFeedback = Feedback.enumerateFeedback(d);
    }

    public float calcExpectedSize(int guess, int[] secrets, int d, int total, int[] feedbackFreq) {

        int[] colorFreqCounter = new int[10];
        for (int secret: secrets) {
            int feedback = Feedback.getFeedback(guess, secret, d, colorFreqCounter);
            feedbackFreq[feedback]++;
        }

        int sum = 0;
        int freq;
        for (int feedback: validFeedback) {
            freq = feedbackFreq[feedback];
            sum += freq * freq;
            feedbackFreq[feedback] = 0;
        }

        return (float) sum / total;
    }
}
