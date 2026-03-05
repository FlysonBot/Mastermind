package org.mastermind;

import org.mastermind.codes.ConvertCode;
import org.mastermind.compute.ExpectedSize;
import org.mastermind.compute.SolutionSpace;
import org.mastermind.solver.BestFirstGuess;
import org.mastermind.solver.BestGuess;
import org.mastermind.solver.GuessStrategy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * MastermindSession manages the full state of a single Mastermind game.
 * It tracks the history of guesses and feedbacks, maintains the solution
 * space of remaining valid secrets, and suggests optimal guesses.
 *
 * <p>Guess and secret array selection is delegated to {@link GuessStrategy},
 * which can be edited independently to change strategy behavior.
 * </p>
 */
public final class MastermindSession {

    private final int           c;
    private final int           d;
    private final int           winFeedback;        // d*10 — all d pegs correct
    private final SolutionSpace solutionSpace;
    private final List<int[]>   history;    // each element: {guess, feedback}
    private       boolean       solved;

    /**
     * Create a new Mastermind session.
     *
     * @param c number of colors (1–9)
     * @param d number of digit positions (1–9)
     */
    public MastermindSession(int c, int d) {
        this.c = c;
        this.d = d;
        this.winFeedback = d * 10;
        this.solutionSpace = new SolutionSpace(c, d);
        this.history = new ArrayList<>();
        this.solved = false;
    }

    /**
     * Suggest the best next guess for the current game state.
     *
     * <p>Array selection (which candidates to evaluate and which secrets to score
     * against) is handled by {@link GuessStrategy}. If only one secret remains,
     * it is returned immediately without invoking the BestGuess search.
     *
     * @return the recommended guess as a code index (0-based, base-c encoding)
     * @throws IllegalStateException if the game is already solved
     */
    public int suggestGuess() {
        return (int) suggestGuessWithDetails()[0];
    }

    /**
     * Suggest the best next guess and return scoring details for display.
     *
     * <p>Use the rank and scoring secrets length to compute an accurate expected
     * size via {@link ExpectedSize#convertSampleRankToExpectedSize(long, int, int)},
     * passing the full solution space size as {@code populationSize}.
     *
     * @return long[] where [0]=guess, [1]=rank, [2]=scoring secrets length
     * @throws IllegalStateException if the game is already solved
     */
    public long[] suggestGuessWithDetails() {
        if (solved) throw new IllegalStateException("Game is already solved.");

        if (history.isEmpty()) {
            long[] first = BestFirstGuess.of(c, d);
            return new long[] {
                    ConvertCode.toIndex(c, d, (int) first[0]), first[1], (long) solutionSpace.getSize()
            };
        }

        if (solutionSpace.getSize() == 1) {
            int[] only = solutionSpace.getSecrets();
            return new long[] { only[0], 1L, 1L };
        }

        int[][] searchSpace = GuessStrategy.select(c, d, solutionSpace);  // {guesses, secrets}
        long[]  result      = BestGuess.findBestGuess(searchSpace[0], searchSpace[1], c, d);
        return new long[] { result[0], result[1], searchSpace[1].length };    // {guess, rank, secrets length}
    }

    /**
     * Record a guess and its feedback, then update the solution space.
     *
     * @param guess    the guess as a code index (0-based, base-c encoding)
     * @param feedback feedback from the game master (black*10 + white)
     * @throws IllegalStateException    if the game is already solved
     * @throws IllegalArgumentException if the feedback leaves no valid secrets
     */
    public void recordGuess(int guess, int feedback) {
        if (solved) throw new IllegalStateException("Game is already solved.");

        history.add(new int[] { guess, feedback });

        // If game is solved, skip filtering directly
        if (feedback == winFeedback) {
            solved = true;
            return;
        }

        // Otherwise filter solution space
        solutionSpace.filterSolution(guess, feedback);

        // Handle error case when no solution remains
        if (solutionSpace.getSize() == 0) {
            throw new IllegalArgumentException(
                    "No valid secrets remain. The feedback provided may be inconsistent with prior guesses.");
        }
    }

    /**
     * Undo the last {@code n} recorded guesses, reconstructing the solution space
     * by replaying the remaining history from scratch.
     *
     * @param n number of guesses to undo (must be &gt;= 1 and &lt;= turn count)
     * @throws IllegalArgumentException if {@code n} is out of range
     */
    public void undo(int n) {
        if (n < 1 || n > history.size())
            throw new IllegalArgumentException("n must be between 1 and " + history.size() + ".");

        int         keep = history.size() - n;
        List<int[]> kept = new ArrayList<>(history.subList(0, keep));

        // Reconstruct solution space from the beginning
        solutionSpace.reset();
        for (int[] entry : kept) {
            solutionSpace.filterSolution(entry[0], entry[1]);
        }

        history.clear();
        history.addAll(kept);
        solved = false;
    }

    /** @return {@code true} if the secret has been identified */
    public boolean isSolved() { return solved; }

    /** @return number of guesses recorded so far */
    public int getTurnCount() { return history.size(); }

    /** @return number of secrets still consistent with all received feedback */
    public int getSolutionSpaceSize() { return solutionSpace.getSize(); }

    /** @return secrets still consistent with all received feedback */
    public int[] getSolutionSpaceSecrets() { return solutionSpace.getSecrets(); }

    /**
     * @return unmodifiable view of the guess history;
     * each element is a two-element array {@code {guess, feedback}}
     */
    public List<int[]> getHistory() { return Collections.unmodifiableList(history); }

    /** @return number of colors in this game */
    public int getC() { return c; }

    /** @return number of digit positions in this game */
    public int getD() { return d; }
}
