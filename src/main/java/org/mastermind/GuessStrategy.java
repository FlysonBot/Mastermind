package org.mastermind;

import org.mastermind.codes.CodeCache;
import org.mastermind.codes.SampledCode;
import org.mastermind.solver.Feedback;

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
     * First turn: always use canonical forms as guesses (exploit full color/position symmetry).
     * Fall back to a Monte Carlo sample for secrets if the product exceeds the threshold.
     * Tries progressively looser tolerances: 0.001, 0.005, then 0.01.
     */
    private static int[][] firstTurn(int c, int d, int[] secrets) {
        int[] canonical = CodeCache.getCanonical(c, d);

        if (fits(canonical.length, secrets.length)) return pair(canonical, secrets);

        for (double tolerance : new double[] { 0.001, 0.005 }) {
            if (fits(canonical.length, secretSampleSize(d, tolerance))) {
                return pair(canonical, secretSample(c, d, tolerance));
            }
        }

        return pair(canonical, secretSample(c, d, 0.01));
    }

    /**
     * Later turns: cascade through several levels of size reduction until the
     * search space fits within the threshold.
     */
    private static int[][] laterTurns(int c, int d, int[] secrets) {
        int[] allValid = CodeCache.getAllValid(c, d);

        if (fits(allValid.length, secrets.length)) return pair(allValid, secrets);
        if (fits(secrets.length, secrets.length)) return pair(secrets, secrets);

        for (double tolerance : new double[] { 0.001, 0.005, 0.01 }) {
            if (fits(secrets.length, secretSampleSize(d, tolerance))) {
                return pair(secrets, secretSample(c, d, tolerance));
            }
        }

        int[] sSample = secretSample(c, d, 0.01);
        for (double percentile : new double[] { 0.001, 0.005, 0.01, 0.05 }) {
            if (fits(secrets.length, guessSampleSize(percentile))) {
                return pair(guessSample(c, d, percentile), sSample);
            }
        }

        return pair(guessSample(c, d, 0.01), sSample);
    }

    private static boolean fits(int guessSpaceSize, int secretSpaceSize) {
        return (long) guessSpaceSize * secretSpaceSize <= THRESHOLD;
    }

    private static int[][] pair(int[] guesses, int[] secrets) {
        return new int[][] { guesses, secrets };
    }

    private static int secretSampleSize(int d, double tolerance) {
        return SampledCode.calcSampleSizeForSecrets(Feedback.calcFeedbackSize(d), tolerance);
    }

    private static int guessSampleSize(double percentileThreshold) {
        return SampledCode.calcSampleSizeForGuesses(percentileThreshold, 0.999);
    }

    private static int[] secretSample(int c, int d, double tolerance) {
        return SampledCode.getSample(c, d, secretSampleSize(d, tolerance));
    }

    private static int[] guessSample(int c, int d, double percentileThreshold) {
        return SampledCode.getSample(c, d, guessSampleSize(percentileThreshold));
    }
}
