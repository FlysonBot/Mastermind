package org.mastermind;

import org.mastermind.codes.AllValidCode;
import org.mastermind.codes.CanonicalCode;
import org.mastermind.codes.SampledCode;
import org.mastermind.solver.Feedback;
import org.mastermind.solver.SolutionSpace;

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
     * @param c             number of colors
     * @param d             number of digits
     * @param turn          0-indexed turn number (0 = first guess)
     * @param solutionSpace current solution space
     * @return int[][] where [0]=guesses, [1]=secrets
     */
    public static int[][] select(int c, int d, int turn, SolutionSpace solutionSpace) {
        int secretsSize = solutionSpace.getSize();
        if (turn == 0) return firstTurn(c, d, secretsSize, solutionSpace);
        return laterTurns(c, d, secretsSize, solutionSpace);
    }

    /**
     * First turn: always use canonical forms as guesses (exploit full color/position symmetry).
     * Fall back to a Monte Carlo sample for secrets if the product exceeds the threshold.
     * Tries progressively looser tolerances: 0.001, 0.005, then 0.01.
     */
    private static int[][] firstTurn(int c, int d, int secretsSize, SolutionSpace solutionSpace) {
        int[] canonical = CanonicalCode.enumerateCanonicalForms(c, d);

        if (fits(canonical.length, secretsSize)) return pair(canonical, solutionSpace.getSecrets());

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
    private static int[][] laterTurns(int c, int d, int secretsSize, SolutionSpace solutionSpace) {

        if (fits((int) Math.pow(c, d), secretsSize))
            return pair(AllValidCode.generateAllCodes(c, d), solutionSpace.getSecrets());
        if (fits(secretsSize, secretsSize)) return pair(solutionSpace.getSecrets(), solutionSpace.getSecrets());

        for (double tolerance : new double[] { 0.001, 0.005, 0.01 }) {
            if (fits(secretsSize, secretSampleSize(d, tolerance))) {
                return pair(solutionSpace.getSecrets(), secretSample(c, d, tolerance));
            }
        }

        int[] sSample = secretSample(c, d, 0.01);
        for (double percentile : new double[] { 0.001, 0.005, 0.01, 0.05 }) {
            if (fits(secretsSize, guessSampleSize(percentile))) {
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
