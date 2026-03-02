package org.mastermind.solver;

import org.mastermind.codes.ConvertCode;

import java.util.BitSet;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.Future;

/**
 * Solution space refer to the set of remaining valid secrets
 * in a Mastermind game. SolutionSpace keep track of which
 * secret is still a valid solution to the puzzle, allowing
 * progress tracking and calculating the best next move.
 *
 * <p>Internally, a BitSet of size c^d is used so that
 * {@link #filterSolution} clears bits in-place with
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
    private final int    totalCodes;  // c^d
    private final BitSet remaining;   // bit i set  ⟺  ConvertCode.toCode(c, d, i) is still a valid secret
    private       int    size;        // cached cardinality of remaining

    public SolutionSpace(int c, int d) {
        this.c = c;
        this.d = d;
        this.totalCodes = (int) Math.pow(c, d);
        this.remaining = new BitSet(totalCodes);
        remaining.set(0, totalCodes);
        this.size = totalCodes;
    }

    /** Reset the solution space to all valid codes */
    public void reset() {
        remaining.set(0, totalCodes);
        size = totalCodes;
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
        if (size < PARALLEL_THRESHOLD) {
            size -= filterRange(guess, obtainedFeedback, 0, totalCodes);
            return;
        }

        // Split into word-aligned (multiple-of-64) chunks for safe concurrent access.
        int parallelism  = POOL.getParallelism();
        int words        = (totalCodes + 63) >>> 6;          // number of 64-bit words
        int wordsPerTask = Math.max(1, (words + parallelism - 1) / parallelism);

        // Submit all tasks except the last; run the last chunk on the calling thread.
        @SuppressWarnings("unchecked")
        Future<Integer>[] futures = new Future[parallelism];
        int fromIndex = 0;
        int taskCount = 0;
        while (fromIndex + wordsPerTask * 64 < totalCodes) {
            final int from = fromIndex;
            final int to   = fromIndex + wordsPerTask * 64;
            futures[taskCount++] = POOL.submit(() -> filterRange(guess, obtainedFeedback, from, to));
            fromIndex = to;
        }

        // Run the tail on the calling thread and sum removed counts.
        int removed = filterRange(guess, obtainedFeedback, fromIndex, totalCodes);

        // Wait for all submitted tasks and accumulate removed counts.
        for (int i = 0; i < taskCount; i++) {
            try { removed += futures[i].get(); } catch (Exception e) { throw new RuntimeException(e); }
        }
        size -= removed;
    }

    /**
     * Single-threaded filter over indices {@code [from, to)}.
     * Safe to call from multiple threads as long as the index ranges are word-aligned
     * (multiples of 64) and disjoint, since each BitSet word is only touched by one thread.
     *
     * @return number of bits cleared
     */
    private int filterRange(int guess, int obtainedFeedback, int from, int to) {
        int[] colorFreqCounter = new int[10];
        int   removed          = 0;
        for (int i = remaining.nextSetBit(from); i >= 0 && i < to; i = remaining.nextSetBit(i + 1)) {
            if (Feedback.getFeedback(guess, ConvertCode.toCode(c, d, i), c, d, colorFreqCounter) != obtainedFeedback) {
                remaining.clear(i);
                removed++;
            }
        }
        return removed;
    }

    /**
     * Materialize the remaining valid secrets as an int array.
     * Called once per turn suggestion, not per filter.
     *
     * @return int array of currently valid secrets
     */
    public int[] getSecrets() {
        int[] secrets = new int[size];
        int   j       = 0;
        for (int i = remaining.nextSetBit(0); i >= 0; i = remaining.nextSetBit(i + 1)) {
            secrets[j++] = ConvertCode.toCode(c, d, i);
        }
        return secrets;
    }

    /**
     * @return size of the current solution space (or valid secrets)
     */
    public int getSize() { return size; }
}
