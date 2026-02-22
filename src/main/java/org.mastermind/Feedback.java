package org.mastermind;

public class Feedback { // Can possibly be implemented faster with int[] if reuse array for guess/secret
    // Reusable arrays
    private final int[] color_freq_counter = new int[] {0, 0, 0, 0, 0, 0, 0, 0, 0};  // 9 zeros
    private final int[] result = new int[2];
    private final int c;
    private final int d;

    public Feedback(int c, int d) {
        if (c > 9 || d > 9) {
            throw new IllegalArgumentException("c or d cannot be larger than 9");
        }

        this.c = c;
        this.d = d;
    }

    public int[] getFeedback(int guess, int secret) {
        int black = 0;
        int color_freq_total = 0;
        int c = this.c;
        int d = this.d;

        for (int i = 0; i < d; i++) {
            // Extract each digit from the guess and secret
            int curr_guess = guess % 10;
            int curr_secret = secret % 10;
            guess /= 10;
            secret /= 10;

            // Either increment black or color_freq
            if (curr_guess == curr_secret) {
                black++;
            } else {
                color_freq_counter[curr_guess - 1]++;
                color_freq_counter[curr_secret - 1]--;
            }
        }

        // Calculate white count from color_freq
        int freq;
        for (int j = 0; j < c; j++) {
            freq = color_freq_counter[j];
            if (freq > 0) {
                color_freq_total += freq;
            } else {
                color_freq_total -= freq;
            }
            color_freq_counter[j] = 0;  // Reset counter
        }
        
        // Return feedback
        result[0] = black;
        result[1] = d - black - (color_freq_total / 2);
        return result;
    }
}
