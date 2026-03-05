package org.mastermind.compute;

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

    private final int     c;
    private final int     d;
    private final int     totalCodes;           // c^d
    private final BitSet  remaining;            // bit i set  ⟺  index i is still a valid secret
    private       int     size;                 // cached cardinality of remaining
    private       boolean isFirstFilter = true; // flag to use specialized function for first filter

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
        isFirstFilter = true;
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
     * <p>The first call uses an incremental path that avoids recomputing all digit
     * comparisons from scratch for every secret index.
     *
     * @param guessInd         index of the guess code (0-based, base-c encoding)
     * @param obtainedFeedback feedback value (black * 9 + d - colorFreqTotal/2)
     */
    public void filterSolution(int guessInd, int obtainedFeedback) {
        // Read and update flag
        final boolean isFirst = isFirstFilter;
        if (isFirst) isFirstFilter = false;

        // When size is small, go single-threaded
        if (size < PARALLEL_THRESHOLD) {
            size -= isFirst ?
                    filterRangeFirst(guessInd, obtainedFeedback, 0, totalCodes) :
                    filterRange(guessInd, obtainedFeedback, 0, totalCodes);
            return;
        }

        // Split into word-aligned (multiple-of-64) chunks for safe concurrent access.
        int parallelism  = POOL.getParallelism();
        int words        = (totalCodes + 63) >>> 6;
        int wordsPerTask = Math.max(1, (words + parallelism - 1) / parallelism);

        // Multi-threaded route
        @SuppressWarnings("unchecked")
        Future<Integer>[] futures = new Future[parallelism];
        int fromIndex = 0;
        int taskCount = 0;
        while (fromIndex + wordsPerTask * 64 < totalCodes) {
            final int from = fromIndex;
            final int to   = fromIndex + wordsPerTask * 64;

            // Submit the task with the appropriate function
            futures[taskCount++] = isFirst ?
                    POOL.submit(() -> filterRangeFirst(guessInd, obtainedFeedback, from, to)) :
                    POOL.submit(() -> filterRange(guessInd, obtainedFeedback, from, to));

            fromIndex = to;
        }

        // Handle the last chunk in main thread
        int removed = isFirst ?
                filterRangeFirst(guessInd, obtainedFeedback, fromIndex, totalCodes) :
                filterRange(guessInd, obtainedFeedback, fromIndex, totalCodes);

        // Sum up the removed count from other threads
        for (int i = 0; i < taskCount; i++) {
            try { removed += futures[i].get(); } catch (Exception e) { throw new RuntimeException(e); }
        }

        // Update size
        size -= removed;
    }

    /**
     * Single-threaded filter over indices {@code [from, to)}.
     * Safe to call from multiple threads as long as the index ranges are word-aligned
     * (multiples of 64) and disjoint, since each BitSet word is only touched by one thread.
     *
     * @return number of bits cleared
     */
    private int filterRange(int guessInd, int obtainedFeedback, int from, int to) {
        int[] colorFreqCounter = new int[c];
        int   removed          = 0;

        // Call getFeedback for each secret
        for (int i = remaining.nextSetBit(from); i >= 0 && i < to; i = remaining.nextSetBit(i + 1)) {
            if (Feedback.getFeedback(guessInd, i, c, d, colorFreqCounter) != obtainedFeedback) {
                remaining.clear(i);
                removed++;
            }
        }
        return removed;
    }

    /**
     * Incremental single-threaded filter over a contiguous {@code [from, to)} range
     * (used only for the first filter when all bits are set). Iterates every index
     * with a plain for-loop and computes feedback incrementally via
     * {@link FeedbackIncremental#getFeedbackIncremental}.
     *
     * @return number of bits cleared
     */
    private int filterRangeFirst(int guessInd, int obtainedFeedback, int from, int to) {
        FeedbackIncremental.State init             = FeedbackIncremental.setupIncremental(guessInd, from, c, d);
        int[]                     guessDigits      = init.guessDigits();
        int[]                     secretDigits     = init.secretDigits();
        int[]                     colorFreqCounter = init.colorFreqCounter();
        int                       black            = init.black();
        int                       colorFreqTotal   = init.colorFreqTotal();
        int                       feedback0        = black * 9 + d - (colorFreqTotal >>> 1);

        // Handle the first secret in chunk
        int removed = 0;
        if (feedback0 != obtainedFeedback) {
            remaining.clear(from);
            removed++;
        }

        // Handle the remaining secrets
        int[] result = new int[3];
        for (int i = from + 1; i < to; i++) {
            FeedbackIncremental.getFeedbackIncremental(guessDigits, secretDigits, black, colorFreqCounter,
                                                       colorFreqTotal, c, d, result);
            black = result[1];
            colorFreqTotal = result[2];
            if (result[0] != obtainedFeedback) {
                remaining.clear(i);
                removed++;
            }
        }

        return removed;
    }

    /**
     * Materialize the remaining valid secrets as an int array of indices.
     * Called once per turn suggestion, not per filter.
     *
     * @return int array of indices of currently valid secrets
     */
    public int[] getSecrets() {
        int[] secretsInd = new int[size];
        int   j          = 0;
        for (int i = remaining.nextSetBit(0); i >= 0; i = remaining.nextSetBit(i + 1)) {
            secretsInd[j++] = i;
        }
        return secretsInd;
    }

    /** @return size of the current solution space (or valid secrets) */
    public int getSize() { return size; }

    /** @return the underlying BitSet of remaining valid secret indices */
    public BitSet getRemaining() { return remaining; }
}
