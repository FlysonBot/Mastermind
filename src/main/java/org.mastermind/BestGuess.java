package org.mastermind;

import java.util.Arrays;

public class BestGuess {

    /**
     * Find the guess that will minimize the expected size of the solution space
     * after guessing.
     *
     * @param guesses all candidate guesses
     * @param secrets remaining possible secrets
     * @param d       number of digits
     * @return        best guess from all candidates
     */
    public static int findBestGuess(int[] guesses, int[] secrets, int d) {
        ExpectedSize expectedSizeObj = new ExpectedSize(d);
        int[] feedbackFreq = new int[100];

        int bestGuess = -1;
        int bestScore = Integer.MAX_VALUE;

        for (int guess : guesses) {
            // Compute rank
            int score = expectedSizeObj.calcExpectedRank(guess, secrets, d, feedbackFreq);

            // Update rank if found a smaller rank
            if (score < bestScore) {
                bestScore = score;
                bestGuess = guess;
            }
        }

        return bestGuess;
    }

    /**
     * Rank all guesses by the expected size of the solution space after each guess.
     *
     * @param guesses all candidate guesses
     * @param secrets remaining possible secrets
     * @param d       number of digits
     * @return 2D array where each row is {guess, score}, sorted best to worst
     */
    public static float[][] rankGuessesByExpectedSize(int[] guesses, int[] secrets, int d) {
        int n = guesses.length;
        float[] scores = new float[n];
        Integer[] indices = new Integer[n]; // need Integer for custom comparator
        int[] feedbackFreq = new int[100];

        ExpectedSize expectedSizeObj = new ExpectedSize(d);

        // 1. Compute scores
        for (int i = 0; i < n; i++) {
            scores[i] = expectedSizeObj.calcExpectedSize(guesses[i], secrets, d, feedbackFreq);
            indices[i] = i;
        }

        // 2. Sort indices by score (ascending)
        Arrays.sort(indices, (a, b) -> Float.compare(scores[a], scores[b]));

        // 3. Build ranked {guess, score} array
        float[][] ranked = new float[n][2];
        for (int i = 0; i < n; i++) {
            int idx = indices[i];
            ranked[i][0] = guesses[idx];
            ranked[i][1] = scores[idx];
        }

        return ranked;
    }
}
