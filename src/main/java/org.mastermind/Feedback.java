package org.mastermind;

public class Feedback {

    /**
     * @param guess             code, digits 1..c, length d
     * @param secret            code, digits 1..c, length d
     * @param d                 number of digits (<= 9)
     * @param colorFreqCounter  int array of 0 with length c
     */
    public static int getFeedback(int guess, int secret, int d, int[] colorFreqCounter) {
        int black = 0;

        for (int i = 0; i < d; i++) {
            int currGuess = guess % 10;
            int currSecret = secret % 10;
            guess /= 10;
            secret /= 10;

            if (currGuess == currSecret) {
                black++;
            } else {
                colorFreqCounter[currGuess]++;
                colorFreqCounter[currSecret]--;
            }
        }

        // Sum absolute values and reset in one pass
        int colorFreqTotal = 0;
        for (int i = 1; i <= 9; i++) {
            int freq = colorFreqCounter[i];
            if (freq > 0) {
                colorFreqTotal += freq;
            } else {
                colorFreqTotal -= freq;
            }
            colorFreqCounter[i] = 0;
        }

        return black * 9 + d - (colorFreqTotal >>> 1);
    }

    public static int calcFeedbackSize(int d) { return (d + 1) * (d + 2) / 2; }

    public static int[] enumerateFeedback(int d) {
        int[] result = new int[calcFeedbackSize(d)];
        int i=0;

        for (int black=0; black <= d; black++) {
            for (int white=0; white <= d - black; white++) {
                result[i] = black * 10 + white;
                i++;
            }
        }

        return result;
    }
}
