package org.mastermind.compute;

/**
 * Feedback is a crucial part of Mastermind. After each guess being
 * made, a feedback is provided to give clues as to how close the
 * guess is to the actual secret. Feedback consists of 2 values, the
 * black and white counts. The black counts is the number of digits
 * in guess and secret that shares the same value at the same position.
 * The white counts is the number of digits in guess and secret that
 * shares the same value at a different positon. In this program,
 * feedback is represented as a 2-digit integers where the first digit
 * represent the black counts, and the second represents the white.
 */
public final class Feedback {

    /**
     * Calculate the Mastermind feedback for a guess and a secret.
     *
     * @param guessInd         index of the guess code (0-based, base-c encoding)
     * @param secretInd        index of the secret code (0-based, base-c encoding)
     * @param c                number of colors (<= 9)
     * @param d                number of digits (<= 9)
     * @param colorFreqCounter int array of 0 with length c
     * @return Feedback value (black * 10 + white)
     */
    public static int getFeedback(int guessInd, int secretInd, int c, int d, int[] colorFreqCounter) {
        int black = 0;

        for (int i = 0; i < d; i++) {
            // Extract digits (0..c-1)
            int currGuess  = guessInd % c;
            int currSecret = secretInd % c;
            guessInd /= c;
            secretInd /= c;

            // Increment counters
            if (currGuess == currSecret) {
                black++;
            } else {
                colorFreqCounter[currGuess]++;
                colorFreqCounter[currSecret]--;
            }
            /*
            How the counter algorithm works:
            - Label each digit in guess and secret as black, white, or gray (unmatched).
            - If we incremented the counter for all digits of both guess and secret,
              sum(|counter|) = 2d.
            - Skipping blacks reduces it by 2*black. Now sum(|counter|) = 2d - 2*black
            - If there is a partial match (white), incrementing for guess and decrementing
              for secret will cause it to cancel out, reducing sum by 2*white
            - So: sum(|coutner|) = 2d - 2*black - 2*white
                  2*white = 2d - 2*black - sum(|counter|)
                  white = d - black - sum(|counter|) / 2
             */
        }

        // Sum absolute values and reset in one pass
        int colorFreqTotal = 0;
        for (int i = 0; i < c; i++) {
            int freq = colorFreqCounter[i];
            colorFreqCounter[i] = 0;
            colorFreqTotal += (freq > 0) ? freq : -freq;
        }

        // black * 10 + white
        // black * 10 + d - black - colorFreqTotal / 2
        // black * 9 + d - colorFreqTotal / 2
        return black * 9 + d - (colorFreqTotal >>> 1);
    }

    /**
     * @param d number of digits in the Mastermind game
     * @return Number of possible feedback values in the game
     */
    public static int calcFeedbackSize(int d) {
        // Feedback values are (b, w) pairs where b + w <= d.
        // Count: for each b in [0..d], there are (d - b + 1) valid w values.
        // Total = sum_{b=0}^{d} (d - b + 1) = (d+1) + d + ... + 1 = (d+1)(d+2)/2.
        return (d + 1) * (d + 2) / 2;
    }

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
