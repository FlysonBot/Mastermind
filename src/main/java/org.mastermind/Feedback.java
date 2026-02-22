package org.mastermind;

public class Feedback {

    /**
     * @param guess  code, digits 1..c, length d
     * @param secret code, digits 1..c, length d
     * @param c      number of colors (<= 9)
     * @param d      number of digits (<= 9)
     */
    public int getFeedback(int guess, int secret, int c, int d) {
        int black = 0;
        int colorFreqTotal = 0;

        if (c > 9 || d > 9) {
            throw new IllegalArgumentException("c or d cannot be larger than 9");
        }

        // Color frequency counter (for color 1-9)
        // Use 9 local int is faster than using an int[]
        int f1 = 0; int f2 = 0; int f3 = 0;
        int f4 = 0; int f5 = 0; int f6 = 0;
        int f7 = 0; int f8 = 0; int f9 = 0;

        int currGuess;
        int currSecret;
        for (int i = 0; i < d; i++) {
            // Extract each digit from the guess and secret
            currGuess = guess % 10;
            currSecret = secret % 10;
            guess /= 10;
            secret /= 10;

            // Either increment black or color frequency counter
            if (currGuess == currSecret) {
                black++;

            } else {
                // Increment counter fi for currGuess = i
                switch (currGuess) {
                    case 1: f1++; break; case 2: f2++; break; case 3: f3++; break;
                    case 4: f4++; break; case 5: f5++; break; case 6: f6++; break;
                    case 7: f7++; break; case 8: f8++; break; case 9: f9++; break;
                }
                // Decrement counter fi for currSecret = i
                switch (currSecret) {
                    case 1: f1--; break; case 2: f2--; break; case 3: f3--; break;
                    case 4: f4--; break; case 5: f5--; break; case 6: f6--; break;
                    case 7: f7--; break; case 8: f8--; break; case 9: f9--; break;
                }
            }
        }

        // Calculate total frequency by summing the absolute value of each f_i
        if (f1 > 0) colorFreqTotal += f1; else colorFreqTotal -= f1;
        if (f2 > 0) colorFreqTotal += f2; else colorFreqTotal -= f2;
        if (f3 > 0) colorFreqTotal += f3; else colorFreqTotal -= f3;
        if (f4 > 0) colorFreqTotal += f4; else colorFreqTotal -= f4;
        if (f5 > 0) colorFreqTotal += f5; else colorFreqTotal -= f5;
        if (f6 > 0) colorFreqTotal += f6; else colorFreqTotal -= f6;
        if (f7 > 0) colorFreqTotal += f7; else colorFreqTotal -= f7;
        if (f8 > 0) colorFreqTotal += f8; else colorFreqTotal -= f8;
        if (f9 > 0) colorFreqTotal += f9; else colorFreqTotal -= f9;

        // Return feedback (black, white) as 2 digit int
        // black * 10 + white = black * 10 + d - black - (colorFreqTotal / 2)
        return black * 9 + d - (colorFreqTotal >>> 1); // '>>> 1' = divide by 2
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
