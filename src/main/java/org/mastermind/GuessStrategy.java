package org.mastermind;

/**
 * Selects which arrays to pass as guesses and secrets to BestGuess for each turn.
 *
 * <p>Returns {@code int[][] { guesses, secrets }} where:
 * <ul>
 *   <li>{@code [0]} — candidate guesses to evaluate</li>
 *   <li>{@code [1]} — secrets used to score each guess</li>
 * </ul>
 *
 * <p>Edit this class to change strategy behavior. {@link #select} dispatches to
 * a private method per turn phase; add new phases or conditions there.
 *
 * <p>Threshold: {@code guesses.length × secrets.length} above which the
 * parallel BestGuess search exceeds ~1 second on the target machine.
 */
public class GuessStrategy {

    private static final long THRESHOLD = 130_000_000L;

    /**
     * Select the guesses and secrets arrays for the current turn.
     *
     * @param c       number of colors
     * @param d       number of digits
     * @param turn    0-indexed turn number (0 = first guess)
     * @param secrets current remaining valid secrets (from SolutionSpace)
     * @return int[][] where [0]=guesses, [1]=secrets
     */
    public static int[][] select(int c, int d, int turn, int[] secrets) {
        if (turn == 0) return firstTurn(c, d, secrets);
        return laterTurns(c, d, secrets);
    }

    /**
     * First turn: always use canonical forms as guesses (exploit full color/position
     * symmetry). Fall back to a Monte Carlo sample for secrets if the product exceeds
     * the threshold.
     */
    private static int[][] firstTurn(int c, int d, int[] secrets) {
        int[] canonicalCodes = CodeCache.getCanonical(c, d);
        if ((long) canonicalCodes.length * secrets.length <= THRESHOLD) {
            return new int[][] { canonicalCodes, secrets };
        }
        return new int[][] { canonicalCodes, sample(c, d) };
    }

    /**
     * Later turns: cascade through several levels of size reduction until the
     * product fits within the threshold.
     *
     * <ol>
     *   <li>All valid codes × remaining secrets — best guess quality.</li>
     *   <li>Remaining secrets × remaining secrets — restrict guess space.</li>
     *   <li>Remaining secrets × sampled secrets — estimate when both are large.</li>
     *   <li>Sampled guesses × sampled secrets — final fallback.</li>
     * </ol>
     */
    private static int[][] laterTurns(int c, int d, int[] secrets) {
        int[] allValidCodes = CodeCache.getAllValid(c, d);

        // If possible, go for the full search space
        if ((long) allValidCodes.length * secrets.length <= THRESHOLD) {
            return new int[][] { allValidCodes, secrets };
        }

        // Otherwise, try restricting guess space to valid solution only
        if ((long) secrets.length * secrets.length <= THRESHOLD) {
            return new int[][] { secrets, secrets };
        }

        int[] randomSample = sample(c, d);
        int   sampleSize   = randomSample.length;

        // If still can't make it, use random sample for secrets
        if ((long) secrets.length * sampleSize <= THRESHOLD) {
            // Remaining secrets × sampled secrets
            return new int[][] { secrets, randomSample };
        }

        // As a last resort, use random sample for both guesses and secrets
        return new int[][] { randomSample, randomSample };
    }

    private static int[] sample(int c, int d) {
        int size = SampledCode.calcSampleSize(Feedback.calcFeedbackSize(d));
        return SampledCode.getSample(c, d, size);
    }
}
