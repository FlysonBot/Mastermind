package org.mastermind.compute;

/**
 * Incremental feedback computation for sequential secret iteration.
 * Extracted from {@link Feedback} to keep that class focused on the
 * stateless per-call computation.
 */
public final class FeedbackIncremental {

    /**
     * Set up the incremental state for the given guess and starting secret index.
     * Extracts guess digits and walks {@code secretInd} digit-by-digit, leaving
     * {@code colorFreqCounter} in persistent non-zeroed form ready for
     * {@link #getFeedbackIncremental}.
     *
     * @param guessInd  index of the guess code (0-based, base-c encoding)
     * @param secretInd index of the starting secret code
     * @param c         number of colors
     * @param d         number of digits
     * @return initial {@link State} for this (guessInd, secretInd) pair
     */
    public static State setupIncremental(int guessInd, int secretInd, int c, int d) {
        int[] guessDigits      = new int[d];
        int[] secretDigits     = new int[d];
        int[] colorFreqCounter = new int[c];

        // Extract guess digits
        int tmp = guessInd;
        for (int p = 0; p < d; p++) {
            guessDigits[p] = tmp % c;
            tmp /= c;
        }

        // Extract secret digits and update colorFreqCounter
        int black = 0;
        tmp = secretInd;
        for (int p = 0; p < d; p++) {
            int gs = guessDigits[p];
            int ss = tmp % c;
            tmp /= c;
            secretDigits[p] = ss;
            if (gs == ss) {
                black++;
            } else {
                colorFreqCounter[gs]++;
                colorFreqCounter[ss]--;
            }
        }

        // Compute colorFreqTotal
        int colorFreqTotal = 0;
        for (int i = 0; i < c; i++) {
            int freq = colorFreqCounter[i];
            colorFreqTotal += freq > 0 ? freq : -freq;
        }

        return new State(guessDigits, secretDigits, colorFreqCounter, black, colorFreqTotal);
    }

    /**
     * Incremental variant of getFeedback for sequential secret iteration (0, 1, 2, ...).
     *
     * <p>Requires that secretDigits[] was correctly set up for the previous secretInd,
     * and that colorFreqCounter[] reflects the contribution of those previous secret
     * digits (without zeroing between calls). On each call, this method:
     * <ol>
     *   <li>Detects which digit positions changed via base-c carry chain</li>
     *   <li>Undoes the contribution of changed positions from colorFreqCounter and black</li>
     *   <li>Updates secretDigits[] for changed positions</li>
     *   <li>Applies new contributions to colorFreqCounter and black</li>
     *   <li>Recomputes colorFreqTotal and returns feedback alongside new black count</li>
     * </ol>
     *
     * @param guessDigits      pre-extracted guess digits [position 0..d-1], position 0 = LSD
     * @param secretDigits     mutable secret digits array, updated in-place
     * @param black            current black count (from previous call)
     * @param colorFreqCounter persistent frequency-difference array, length c (NOT cleared between calls)
     * @param colorFreqTotal   current sum of |colorFreqCounter[i]|, updated in-place
     * @param c                number of colors
     * @param d                number of digits
     * @param result           int[3] output buffer: result[0]=feedback, result[1]=new black count,
     *                         result[2]=new colorFreqTotal
     */
    public static void getFeedbackIncremental(
            int[] guessDigits, int[] secretDigits, int black, int[] colorFreqCounter,
            int colorFreqTotal, int c, int d, int[] result
    ) {
        // Walk the base-c carry chain: increment secretDigits in-place
        for (int p = 0; p < d; p++) {
            // Extract digits
            int oldDigit = secretDigits[p];
            int newDigit = oldDigit == c - 1 ? 0 : oldDigit + 1;
            int gDigit   = guessDigits[p];
            secretDigits[p] = newDigit;

            // Update colorFreqCounter and colorFreqTotal
            int v;
            if (gDigit == oldDigit) {
                // Was black, now not: black--, apply newDigit contribution
                black--;
                v = colorFreqCounter[gDigit];
                colorFreqTotal += (v >= 0 ? 1 : -1);
                colorFreqCounter[gDigit] = v + 1;
                v = colorFreqCounter[newDigit];
                colorFreqTotal += (v <= 0 ? 1 : -1);
                colorFreqCounter[newDigit] = v - 1;
            } else if (gDigit == newDigit) {
                // Was not black, now black: black++, undo oldDigit contribution
                black++;
                v = colorFreqCounter[gDigit];
                colorFreqTotal += (v <= 0 ? 1 : -1);
                colorFreqCounter[gDigit] = v - 1;
                v = colorFreqCounter[oldDigit];
                colorFreqTotal += (v >= 0 ? 1 : -1);
                colorFreqCounter[oldDigit] = v + 1;
            } else {
                // Neither black: gDigit updates cancel, only oldDigit and newDigit change
                v = colorFreqCounter[oldDigit];
                colorFreqTotal += (v >= 0 ? 1 : -1);
                colorFreqCounter[oldDigit] = v + 1;
                v = colorFreqCounter[newDigit];
                colorFreqTotal += (v <= 0 ? 1 : -1);
                colorFreqCounter[newDigit] = v - 1;
            }

            // When newDigit != 0, no carry propagates to the next position,
            // meaning all higher positions are unchanged. Break early.
            if (newDigit != 0) break;
        }

        // Update result
        result[0] = black * 9 + d - (colorFreqTotal >>> 1);
        result[1] = black;
        result[2] = colorFreqTotal;
    }

    /**
     * Snapshot of the incremental state for a given (guessInd, secretInd) pair.
     * Used to bootstrap {@link #getFeedbackIncremental} for the next secret index.
     */
    public record State(int[] guessDigits, int[] secretDigits, int[] colorFreqCounter,
                        int black, int colorFreqTotal
    ) { }
}
