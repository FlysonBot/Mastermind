package org.mastermind.solver;

import org.mastermind.codes.CodeCache;

/**
 * Solution space refer to the set of remaining valid secrets
 * in a Mastermind game. SolutionSpace keep track of which
 * secret is still a valid solution to the puzzle, allowing
 * progress tracking and calculating the best next move.
 */
public class SolutionSpace {
    private final int   d;
    private       int[] remainingSecrets;

    public SolutionSpace(int c, int d) {
        this.d = d;
        remainingSecrets = CodeCache.getAllValid(c, d).clone();
    }

    /**
     * Reset the solution space to all valid codes for the given number of colors.
     *
     * @param c number of colors
     */
    public void reset(int c) {
        remainingSecrets = CodeCache.getAllValid(c, d).clone();
    }

    /**
     * Filter the solution space according to the obtained feedback from a guess.
     * After this operation, only the secrets whose feedback with the input guess
     * matches the obtained feedback would be kept.
     *
     * @param guess            code, digits 1..c, length d
     * @param obtainedFeedback feedback value (black * 10 + white)
     */
    public void filterSolution(int guess, int obtainedFeedback) {
        int limit = remainingSecrets.length;
        int d     = this.d;

        // Update remainingSecrets so that still valid combinations are in the front
        int   feedback;
        int   replaceInd       = 0;
        int[] colorFreqCounter = new int[10];
        for (int i = 0; i < limit; i++) {
            feedback = Feedback.getFeedback(guess, remainingSecrets[i], d, colorFreqCounter);

            if (feedback == obtainedFeedback) {
                remainingSecrets[replaceInd] = remainingSecrets[i];
                replaceInd++;
            }
        }

        // Extract the valid combinations from the front into a new array
        int[] newRemainingSecrets = new int[replaceInd];
        System.arraycopy(remainingSecrets, 0, newRemainingSecrets, 0, replaceInd);
        remainingSecrets = newRemainingSecrets;
    }

    /**
     * @return int array of currently solution space (or valid secrets)
     */
    public int[] getSecrets() { return remainingSecrets; }

    /**
     * @return size of the current solution space (or valid secrets)
     */
    public int getSize() { return remainingSecrets.length; }

}
