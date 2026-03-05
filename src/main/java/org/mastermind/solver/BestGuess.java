package org.mastermind.solver;

import org.mastermind.compute.ExpectedSize;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * This is a strategy to find the best guess for Mastermind by searching
 * through the space of all candidate guesses and secrets array to find
 * the guess that minimize the average number of remaining solutions to
 * the puzzle. Due to the nature of Mastermind, sometimes the search
 * space can be huge. To optimize for performance, the program create a
 * thread for each CPU thread precent on the machine. The algorithm go
 * multi-threading when the search space exceed a threshold, which is a
 * heuristic value for when the algorithm will take longer than
 * 50 milliseconds to run.
 */
public class BestGuess {
    private static final int             THREAD_COUNT       = Runtime.getRuntime().availableProcessors();
    private static final ExecutorService POOL;
    private static final long            PARALLEL_THRESHOLD = 3_000_000;

    static {
        POOL = Executors.newFixedThreadPool(THREAD_COUNT, r -> {
            Thread t = new Thread(r);
            t.setDaemon(true);
            return t;
        });
    }

    /**
     * Find the guess that will minimize the expected size of the solution space
     * after guessing.
     *
     * @param guessesInd all candidate guess indices (0-based, base-c encoding)
     * @param secretsInd remaining possible secret indices (0-based, base-c encoding)
     * @param c          number of colors (<= 9)
     * @param d          number of digits
     * @return long[] where [0]=best guess index, [1]=its rank (sum of squared partition sizes)
     */
    public static long[] findBestGuess(int[] guessesInd, int[] secretsInd, int c, int d) {

        // Determine whether multi-threading is needed
        if ((long) guessesInd.length * secretsInd.length < PARALLEL_THRESHOLD) {
            return findBestGuessAlgorithm(guessesInd, secretsInd, c, d, 0, guessesInd.length);
        }

        // Call the parallelized version of the algorithm
        return findBestGuessParallel(guessesInd, secretsInd, c, d);
    }

    // Provide a way to force specific algorithm choice for benchmarking
    public static long[] findBestGuess(int[] guessesInd, int[] secretsInd, int c, int d, boolean parallel) {
        if (!parallel) return findBestGuessAlgorithm(guessesInd, secretsInd, c, d, 0, guessesInd.length);
        return findBestGuessParallel(guessesInd, secretsInd, c, d);
    }

    private static long[] findBestGuessParallel(int[] guessesInd, int[] secretsInd, int c, int d) {

        // Calculate the chunk size with ceil(guessesInd.length / THREAD_COUNT)
        int chunkSize     = (guessesInd.length + THREAD_COUNT - 1) / THREAD_COUNT;
        int actualThreads = (guessesInd.length + chunkSize - 1) / chunkSize;

        // Initialize futures list (holder for pending thread outputs)
        List<Future<long[]>> futures = new ArrayList<>(actualThreads);

        // Submit work to each threads
        for (int t = 0; t < actualThreads; t++) {
            final int from = t * chunkSize;
            final int to   = Math.min(from + chunkSize, guessesInd.length);
            futures.add(t, POOL.submit(() -> findBestGuessAlgorithm(guessesInd, secretsInd, c, d, from, to)));
        }

        // Find best guess from returned result
        int  bestGuessInd = -1;
        long bestScore    = Long.MAX_VALUE;

        for (Future<long[]> future : futures) {
            try {
                // Read the result
                long[] result = future.get();

                // Update best guess if found better score
                if (result[1] < bestScore) {
                    bestGuessInd = (int) result[0];
                    bestScore = result[1];
                }

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted while waiting for thread result", e);
            } catch (ExecutionException e) {
                throw new RuntimeException("Exception in worker thread", e.getCause());
            }
        }

        return new long[] { bestGuessInd, bestScore };
    }

    private static long[] findBestGuessAlgorithm(int[] guessesInd, int[] secretsInd, int c, int d, int start, int end) {
        ExpectedSize expectedSizeObj = new ExpectedSize(d);
        int[]        feedbackFreq    = new int[100];

        int  bestGuessInd = -1;
        long bestScore    = Long.MAX_VALUE;

        for (int i = start; i < end; i++) {
            // Compute rank
            int  guessInd = guessesInd[i];
            long score    = expectedSizeObj.calcExpectedRank(guessInd, secretsInd, c, d, feedbackFreq);

            // Update result if found a smaller rank
            if (score < bestScore) {
                bestScore = score;
                bestGuessInd = guessInd;
            }
        }

        return new long[] { bestGuessInd, bestScore };
    }
}
