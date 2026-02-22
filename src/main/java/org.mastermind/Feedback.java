package org.mastermind;

public class Feedback {
    private final int[] _result = new int[2];  // Reuse array avoid allocation in loop

    /**
     * @param guess  code, digits 1..c, length d
     * @param secret code, digits 1..c, length d
     * @param c      number of colors (<= 9)
     * @param d      number of digits (<= 9)
     */
    public int[] getFeedback(int guess, int secret, int c, int d) {
        int black = 0;
        int color_freq_total = 0;
        int[] result = this._result;

        if (c > 9 || d > 9) {
            throw new IllegalArgumentException("c or d cannot be larger than 9");
        }

        // Color frequency counter (for color 1-9)
        // Use 9 local int is faster than using an int[]
        int f1 = 0; int f2 = 0; int f3 = 0;
        int f4 = 0; int f5 = 0; int f6 = 0;
        int f7 = 0; int f8 = 0; int f9 = 0;

        int curr_guess;
        int curr_secret;
        for (int i = 0; i < d; i++) {
            // Extract each digit from the guess and secret
            curr_guess = guess % 10;
            curr_secret = secret % 10;
            guess /= 10;
            secret /= 10;

            // Either increment black or color frequency counter
            if (curr_guess == curr_secret) {
                black++;

            } else {
                // Increment counter fi for curr_guess = i
                switch (curr_guess) {
                    case 1: f1++; break; case 2: f2++; break; case 3: f3++; break;
                    case 4: f4++; break; case 5: f5++; break; case 6: f6++; break;
                    case 7: f7++; break; case 8: f8++; break; case 9: f9++; break;
                }
                // Decrement counter fi for curr_secret = i
                switch (curr_secret) {
                    case 1: f1--; break; case 2: f2--; break; case 3: f3--; break;
                    case 4: f4--; break; case 5: f5--; break; case 6: f6--; break;
                    case 7: f7--; break; case 8: f8--; break; case 9: f9--; break;
                }
            }
        }

        // Calculate total frequency by summing the absolute value of each f_i
        if (f1 > 0) color_freq_total += f1; else color_freq_total -= f1;
        if (f2 > 0) color_freq_total += f2; else color_freq_total -= f2;
        if (f3 > 0) color_freq_total += f3; else color_freq_total -= f3;
        if (f4 > 0) color_freq_total += f4; else color_freq_total -= f4;
        if (f5 > 0) color_freq_total += f5; else color_freq_total -= f5;
        if (f6 > 0) color_freq_total += f6; else color_freq_total -= f6;
        if (f7 > 0) color_freq_total += f7; else color_freq_total -= f7;
        if (f8 > 0) color_freq_total += f8; else color_freq_total -= f8;
        if (f9 > 0) color_freq_total += f9; else color_freq_total -= f9;

        // Return feedback (black, white)
        result[0] = black;
        result[1] = d - black - (color_freq_total >>> 1); // '>>> 1' = divide by 2
        return result;
    }

    public static int calcFeedbackSize(int d) { return (d + 1) * (d + 2) / 2; }

    public static int[][] enumerateFeedback(int d) {
        int[][] result = new int[calcFeedbackSize(d)][2];
        int i=0;

        for (int black=0; black<d; black++) {
            for (int white=0; white < d - black; white++) {
                result[i] = new int[] {black, white};
                i++;
            }
        }

        return result;
    }
}
