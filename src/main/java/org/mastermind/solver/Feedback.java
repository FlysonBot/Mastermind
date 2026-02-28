package org.mastermind.solver;

/**
 * Feedback is a crucial part of Mastermind. After each guess being
 * made, a feedback is provided to give clues as to how close the
 * guess is to the actual secret. Feedback consists of 2 values, the
 * black and white counts. The black counts is the number of digits
 * in guess and secret that shares the same value at the same position.
 * The white counts is the number of digits in guess and secret that
 * shares the same  value at a different positon. In this program,
 * feedback is represented as a 2-digit integers where the first digit
 * represent the black counts, and the second represents the white.
 */
public final class Feedback {

    /**
     * Calculate the Mastermind feedback for a guess and a secret.
     *
     * @param guess            code, digits 1..c, length d
     * @param secret           code, digits 1..c, length d
     * @param c                number of colors (<= 9)
     * @param d                number of digits (<= 9)
     * @param colorFreqCounter int array of 0 with length c
     * @return Feedback value (black * 10 + white)
     */
    public static int getFeedback(int guess, int secret, int c, int d, int[] colorFreqCounter) {
        int black = 0;

        for (int i = 0; i < d; i++) {
            // Extract digits
            int currGuess  = guess % 10;
            int currSecret = secret % 10;
            guess /= 10;
            secret /= 10;

            // Increment counters
            if (currGuess == currSecret) {
                black++;
            } else {
                colorFreqCounter[currGuess]++;
                colorFreqCounter[currSecret]--;
            }
        }

        // Sum absolute values and reset in one pass
        int colorFreqTotal = 0;
        for (int i = 1; i <= c; i++) {
            int freq = colorFreqCounter[i];
            colorFreqCounter[i] = 0;
            colorFreqTotal += (freq > 0) ? freq : -freq;
        }

        // black * 10 + d - black - colorFreqTotal / 2
        return black * 9 + d - (colorFreqTotal >>> 1);
    }

    /**
     * @param d number of digits in the Mastermind game
     * @return Number of possible feedback values in the game
     */
    public static int calcFeedbackSize(int d) { return (d + 1) * (d + 2) / 2; }

    /**
     * @param d number of digits in the Mastermind game
     * @return All possible feedback values in the game
     */
    public static int[] enumerateFeedback(int d) {
        int[] result = new int[calcFeedbackSize(d)];
        int   i      = 0;

        for (int black = 0; black <= d; black++) {
            for (int white = 0; white <= d - black; white++) {
                result[i] = black * 10 + white;
                i++;
            }
        }

        return result;
    }
}
