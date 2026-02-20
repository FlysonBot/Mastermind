public class Feedback {
    private static final int[] color_freq_counter = new int[] {0, 0, 0, 0, 0, 0, 0, 0, 0};  // 9 zeros
    private static final int[] divisors = new int[] {1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000};  // 9 divisors

    public static int[] getFeedback(int guess, int secret, int c, int d) {
        if (c > 9 || d > 9) {
            throw new IllegalArgumentException("c or d cannot be larger than 9");
        }

        int black = 0;
        int color_freq_total = 0;

        for (int i = 0; i < d; i++) {
            // Extract each digit from the guess and secret
            int curr_guess = (int) (guess / divisors[i] % 10);
            int curr_secret = (int) (secret / divisors[i] % 10);

            // Either increment black or color_freq
            if (curr_guess == curr_secret) {
                black++;
            } else {
                color_freq_counter[curr_guess - 1]++;
                color_freq_counter[curr_secret - 1]--;
            }
        }

        // Calculate white count from color_freq
        for (int j = 0; j < c; j++) {
            if (color_freq_counter[j] > 0) {
                color_freq_total += color_freq_counter[j];
            } else {
                color_freq_total -= color_freq_counter[j];
            }
            color_freq_counter[j] = 0;  // Reset counter
        }
        
        // Return feedback
        return new int[] {black, d - black - (color_freq_total / 2)}; // black, white
    }
}
