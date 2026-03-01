package org.mastermind.solver;

import org.mastermind.codes.CodeCache;

import java.util.BitSet;
import java.util.concurrent.ForkJoinPool;

/**
 * Solution space refer to the set of remaining valid secrets
 * in a Mastermind game. SolutionSpace keep track of which
 * secret is still a valid solution to the puzzle, allowing
 * progress tracking and calculating the best next move.
 *
 * <p>Internally, a BitSet indexed over {@code CodeCache.getAllValid(c, d)}
 * is used so that {@link #filterSolution} clears bits in-place with
 * zero allocation. BitSet's nextSetBit iteration also skips eliminated
 * secrets in bulk (64 per word), making repeated filtering fast even
 * when the initial space is large (e.g., 9×9 = 387 M codes).
 */
public class SolutionSpace {
    /** Minimum number of set bits before parallel filtering is used. */
    private static final int          PARALLEL_THRESHOLD = 16384;
    private static final ForkJoinPool POOL               = ForkJoinPool.commonPool();

    private final int    c;
    private final int    d;
    private final int[]  allValid;   // CodeCache.getAllValid(c, d) — index → code value
    private final BitSet remaining;  // bit i set  ⟺  allValid[i] is still a valid secret

    public SolutionSpace(int c, int d) {
        this.c = c;
        this.d = d;
        this.allValid = CodeCache.getAllValid(c, d);
        this.remaining = new BitSet(allValid.length);
        remaining.set(0, allValid.length);
    }

    /** Reset the solution space to all valid codes */
    public void reset() {
        remaining.set(0, allValid.length);
    }

    /**
     * Filter the solution space according to the obtained feedback from a guess.
     * After this operation, only the secrets whose feedback with the input guess
     * matches the obtained feedback would be kept.
     *
     * <p>For large solution spaces (cardinality &ge; {@code PARALLEL_THRESHOLD}),
     * work is split into word-aligned 64-index chunks and processed in parallel
     * via the common ForkJoinPool. Each chunk owns a disjoint word range in the
     * BitSet, so concurrent {@code clear()} calls on non-overlapping words are safe.
     * For small spaces the single-threaded path is used to avoid FJP overhead.
     *
     * @param guess            code, digits 1..c, length d
     * @param obtainedFeedback feedback value (black * 9 + d - colorFreqTotal/2)
     */
    public void filterSolution(int guess, int obtainedFeedback) {
        if (remaining.cardinality() < PARALLEL_THRESHOLD) {
            filterRange(guess, obtainedFeedback, 0, allValid.length);
            return;
        }

        // Split into word-aligned (multiple-of-64) chunks for safe concurrent access.
        int parallelism  = POOL.getParallelism();
        int words        = (allValid.length + 63) >>> 6;          // number of 64-bit words
        int wordsPerTask = Math.max(1, (words + parallelism - 1) / parallelism);

        int fromIndex = 0;
        // Submit all tasks except the last; run the last chunk on the calling thread.
        java.util.concurrent.Future<?>[] futures   = new java.util.concurrent.Future<?>[parallelism];
        int                              taskCount = 0;
        while (fromIndex + wordsPerTask * 64 < allValid.length) {
            final int from = fromIndex;
            final int to   = fromIndex + wordsPerTask * 64;
            futures[taskCount++] = POOL.submit(() -> filterRange(guess, obtainedFeedback, from, to));
            fromIndex = to;
        }

        // Run the tail on the calling thread.
        filterRange(guess, obtainedFeedback, fromIndex, allValid.length);

        // Wait for all submitted tasks.
        for (int i = 0; i < taskCount; i++) {
            try { futures[i].get(); } catch (Exception e) { throw new RuntimeException(e); }
        }
    }

    /**
     * Single-threaded filter over {@code allValid[from..to)}.
     * Safe to call from multiple threads as long as the index ranges are word-aligned
     * (multiples of 64) and disjoint, since each BitSet word is only touched by one thread.
     */
    private void filterRange(int guess, int obtainedFeedback, int from, int to) {
        int[] colorFreqCounter = new int[10];
        for (int i = remaining.nextSetBit(from); i >= 0 && i < to; i = remaining.nextSetBit(i + 1)) {
            if (Feedback.getFeedback(guess, allValid[i], c, d, colorFreqCounter) != obtainedFeedback) {
                remaining.clear(i);
            }
        }
    }

    /**
     * Materialize the remaining valid secrets as an int array.
     * Called once per turn suggestion, not per filter.
     *
     * @return int array of currently valid secrets
     */
    public int[] getSecrets() {
        int   size    = remaining.cardinality();
        int[] secrets = new int[size];
        int   j       = 0;
        for (int i = remaining.nextSetBit(0); i >= 0; i = remaining.nextSetBit(i + 1)) {
            secrets[j++] = allValid[i];
        }
        return secrets;
    }

    /**
     * @return size of the current solution space (or valid secrets)
     */
    public int getSize() { return remaining.cardinality(); }
}
