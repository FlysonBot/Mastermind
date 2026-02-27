package org.mastermind.solver;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * This is a strategy to find the best guess for Mastermind by searching
 * through the space of all valid guesses and secrets to find the guess
 * that minimize the average number of remaining solutions to the puzzle.
 * Due to the nature of Mastermind, sometimes the search space can be huge.
 * To optimize for performance, the program create a thread for each CPU
 * thread precent on the machine. The algorithm go multi-threading when
 * the search space exceed a threshold, which is a heuristic value for
 * when the algorithm will take longer than 50 milliseconds to run.
 */
public class BestGuess {
    private static final int             THREAD_COUNT       = Runtime.getRuntime().availableProcessors();
    private static final ExecutorService POOL               = Executors.newFixedThreadPool(THREAD_COUNT);
    private static final long            PARALLEL_THRESHOLD = 3_000_000;

    public static void shutdown() { POOL.shutdown(); }

    /**
     * Find the guess that will minimize the expected size of the solution space
     * after guessing.
     *
     * @param guesses all candidate guesses
     * @param secrets remaining possible secrets
     * @param d       number of digits
     * @return long[] where [0]=best guess, [1]=its rank (sum of squared partition sizes)
     */
    public static long[] findBestGuess(int[] guesses, int[] secrets, int d) {

        // Determine whether multi-threading is needed
        if ((long) guesses.length * secrets.length < PARALLEL_THRESHOLD) {
            return findBestGuessAlgorithm(guesses, secrets, d, 0, guesses.length);
        }

        // Call the parallelized version of the algorithm
        return findBestGuessParallel(guesses, secrets, d);
    }

    public static long[] findBestGuess(int[] guesses, int[] secrets, int d, boolean parallel) {
        if (!parallel) return findBestGuessAlgorithm(guesses, secrets, d, 0, guesses.length);
        return findBestGuessParallel(guesses, secrets, d);
    }

    private static long[] findBestGuessParallel(int[] guesses, int[] secrets, int d) {

        // Calculate the chunk size with ceil(guesses.length / THREAD_COUNT)
        int chunkSize     = (guesses.length + THREAD_COUNT - 1) / THREAD_COUNT;
        int actualThreads = (guesses.length + chunkSize - 1) / chunkSize;

        // Holder for function's output result
        List<Future<long[]>> futures = new ArrayList<>(actualThreads);

        // Submit work to each threads
        for (int t = 0; t < actualThreads; t++) {
            final int from = t * chunkSize;
            final int to   = Math.min(from + chunkSize, guesses.length);
            futures.add(t, POOL.submit(() -> findBestGuessAlgorithm(guesses, secrets, d, from, to)));
        }

        // Find best guess from returned result
        int  bestGuess = -1;
        long bestScore = Long.MAX_VALUE;

        for (Future<long[]> future : futures) {
            try {
                // Read the result
                long[] result = future.get();

                // Update best guess if found better score
                if (result[1] < bestScore) {
                    bestGuess = (int) result[0];
                    bestScore = result[1];
                }

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted while waiting for thread result", e);
            } catch (ExecutionException e) {
                throw new RuntimeException("Exception in worker thread", e.getCause());
            }
        }

        return new long[] { bestGuess, bestScore };
    }

    private static long[] findBestGuessAlgorithm(int[] guesses, int[] secrets, int d, int start, int end) {
        ExpectedSize expectedSizeObj = new ExpectedSize(d);
        int[]        feedbackFreq    = new int[100];

        int  bestGuess = -1;
        long bestScore = Long.MAX_VALUE;

        for (int i = start; i < end; i++) {
            // Compute rank
            int  guess = guesses[i];
            long score = expectedSizeObj.calcExpectedRank(guess, secrets, d, feedbackFreq);

            // Update result if found a smaller rank
            if (score < bestScore) {
                bestScore = score;
                bestGuess = guess;
            }
        }

        return new long[] { bestGuess, bestScore };
    }

    /**
     * Rank all guesses by the expected size of the solution space after each guess.
     *
     * @param guesses all candidate guesses
     * @param secrets remaining possible secrets
     * @param d       number of digits
     * @return 2D array where each row is {guess, score}, sorted best to worst
     */
    public static float[][] rankGuessesByExpectedSize(int[] guesses, int[] secrets, int d) {
        int       n            = guesses.length;
        float[]   scores       = new float[n];
        Integer[] indices      = new Integer[n]; // need Integer for custom comparator
        int[]     feedbackFreq = new int[100];

        ExpectedSize expectedSizeObj = new ExpectedSize(d);

        // 1. Compute scores
        for (int i = 0; i < n; i++) {
            scores[i] = expectedSizeObj.calcExpectedSize(guesses[i], secrets, d, feedbackFreq);
            indices[i] = i;
        }

        // 2. Sort indices by score (ascending)
        Arrays.sort(indices, (a, b) -> Float.compare(scores[a], scores[b]));

        // 3. Build ranked {guess, score} array
        float[][] ranked = new float[n][2];
        for (int i = 0; i < n; i++) {
            int idx = indices[i];
            ranked[i][0] = guesses[idx];
            ranked[i][1] = scores[idx];
        }

        return ranked;
    }
}
