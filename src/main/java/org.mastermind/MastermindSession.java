package org.mastermind;

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
public class MastermindSession {

    private final int c;
    private final int d;
    private final int winFeedback;        // d*10 — all d pegs correct
    private final SolutionSpace solutionSpace;
    private final List<int[]> history;    // each element: {guess, feedback}
    private boolean solved;

    /**
     * Create a new Mastermind session.
     *
     * @param c  number of colors (1–9)
     * @param d  number of digit positions (1–9)
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
     * @return the recommended guess as an integer code (digits 1..c, length d)
     * @throws IllegalStateException if the game is already solved
     */
    public int suggestGuess() {
        if (solved) throw new IllegalStateException("Game is already solved.");

        int[] secrets = solutionSpace.getSecrets();
        if (secrets.length == 1) return secrets[0];

        int[][] arrays = GuessStrategy.select(c, d, history.size(), secrets);
        return BestGuess.findBestGuess(arrays[0], arrays[1], d);
    }

    /**
     * Record a guess and its feedback, then update the solution space.
     *
     * @param guess     the guessed code (digits 1..c, length d)
     * @param feedback  feedback from the game master (black*10 + white)
     * @throws IllegalStateException    if the game is already solved
     * @throws IllegalArgumentException if the feedback leaves no valid secrets
     */
    public void recordGuess(int guess, int feedback) {
        if (solved) throw new IllegalStateException("Game is already solved.");

        history.add(new int[]{guess, feedback});
        solutionSpace.filterSolution(guess, feedback);

        if (feedback == winFeedback) {
            solved = true;
        } else if (solutionSpace.getSize() == 0) {
            throw new IllegalArgumentException(
                    "No valid secrets remain. The feedback provided may be inconsistent with prior guesses.");
        }
    }

    /**
     * Undo the last {@code n} recorded guesses, reconstructing the solution space
     * by replaying the remaining history from scratch.
     *
     * @param n  number of guesses to undo (must be &gt;= 1 and &lt;= turn count)
     * @throws IllegalArgumentException if {@code n} is out of range
     */
    public void undo(int n) {
        if (n < 1 || n > history.size())
            throw new IllegalArgumentException("n must be between 1 and " + history.size() + ".");

        int keep = history.size() - n;
        List<int[]> kept = new ArrayList<>(history.subList(0, keep));

        // Reconstruct solution space from the beginning
        solutionSpace.reset(c);
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
     *         each element is a two-element array {@code {guess, feedback}}
     */
    public List<int[]> getHistory() { return Collections.unmodifiableList(history); }

    /** @return number of colors in this game */
    public int getC() { return c; }

    /** @return number of digit positions in this game */
    public int getD() { return d; }
}
