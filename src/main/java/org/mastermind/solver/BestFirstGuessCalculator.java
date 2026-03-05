package org.mastermind.solver;

import org.mastermind.codes.CanonicalCode;
import org.mastermind.codes.ConvertCode;
import org.mastermind.codes.SampledCode;

/**
 * Offline calculator for regenerating the hardcoded table in {@link BestFirstGuess}.
 * Not used at runtime — run main() once after algorithm changes to recompute values.
 */
final class BestFirstGuessCalculator {

    // --- Calculation constants ---
    private static final int    TRIALS               = 100;
    private static final long   TARGET_EVALS         = 13_000_000L;
    private static final double CONFIDENCE_THRESHOLD = 99.0;
    private static final int    BUDGET_MULTIPLIER    = 2;

    public static void main(String[] args) {
        int[] feedbackFreq = new int[100];

        // c=1 and d=1 are trivial, calibrate c in [2,9] x d in [2,9]
        int      total    = 8 * 8;
        String[] lines    = new String[total];
        int[][]  bestCode = new int[10][10];
        int      li       = 0;

        String header = String.format("%-6s  %-12s  %10s  %10s  %12s",
                                      "Game", "BestGuess", "AvgScore", "Confidence", "TotalEvals");
        System.out.println(header);
        System.out.println("-".repeat(60));

        for (int c = 2; c <= 9; c++) {
            for (int d = 2; d <= 9; d++) {
                ExpectedSize expectedSize = new ExpectedSize(d);
                int[]        canonical    = CanonicalCode.enumerateCanonicalForms(c, d);
                int          totalCodes   = (int) Math.pow(c, d);

                long   budget = TARGET_EVALS;
                Result result;
                do {
                    result = evaluate(canonical, c, d, totalCodes, budget, feedbackFreq, expectedSize);
                    if (result.confidence < CONFIDENCE_THRESHOLD) {
                        budget *= BUDGET_MULTIPLIER;
                        System.out.printf("  [%dx%d] confidence %.2f%% too low, retrying with budget %d%n",
                                          c, d, result.confidence, budget);
                    }
                } while (result.confidence < CONFIDENCE_THRESHOLD);

                int code = ConvertCode.toCode(c, d, canonical[result.bestIdx]);
                bestCode[c][d] = code;
                lines[li] = String.format("%-6s  %-12d  %10.4f  %9.2f%%  %12d%s",
                                          c + "x" + d, code,
                                          result.avgScore, result.confidence,
                                          result.totalEvals,
                                          result.fullEval ? " (full)" : "");
                System.out.println(lines[li]);
                li++;
            }
        }

        // Clean summary
        System.out.printf("%n%s%n", header);
        System.out.println("-".repeat(60));
        for (String line : lines) System.out.println(line);

        // Phase 2: full evaluation to get true rank for each best guess
        System.out.printf("%n%-6s  %-12s  %s%n", "Game", "BestGuess", "TrueRank");
        System.out.println("-".repeat(35));
        long[][] trueRank = new long[10][10];
        for (int c = 2; c <= 9; c++) {
            for (int d = 2; d <= 9; d++) {
                ExpectedSize expectedSize = new ExpectedSize(d);
                int          totalCodes   = (int) Math.pow(c, d);
                int          codeIndex    = ConvertCode.toIndex(c, d, bestCode[c][d]);
                trueRank[c][d] = expectedSize.calcExpectedRankFirst(codeIndex, c, d, totalCodes, feedbackFreq);
                System.out.printf("%-6s  %-12d  %d%n", c + "x" + d, bestCode[c][d], trueRank[c][d]);
            }
        }

        // Print switch snippet
        System.out.println("\n// --- copy below into of(int c, int d) ---");
        for (int c = 2; c <= 9; c++) {
            System.out.printf("            case %d -> switch (d) {%n", c);
            for (int d = 2; d <= 9; d++) {
                System.out.printf("                case %d -> new long[]{%d, %dL};%n", d, bestCode[c][d],
                                  trueRank[c][d]);
            }
            System.out.printf(
                    "                default -> throw new IllegalArgumentException(\"Unsupported game size: c=\" + c " +
                            "+ \", d=\" + d);%n");
            System.out.printf("            };%n");
        }
        System.out.println("// --- copy above ---");
    }

    static Result evaluate(
            int[] canonical, int c, int d, int totalCodes,
            long budget, int[] feedbackFreq, ExpectedSize expectedSize
    ) {
        int     n          = canonical.length;
        int     sampleSize = Math.max(1, (int) (budget / TRIALS / n));
        boolean fullEval   = sampleSize >= totalCodes;
        int     normSize   = fullEval ? totalCodes : sampleSize;
        int     trials     = fullEval ? 1 : TRIALS;

        double[] sumScore  = new double[n];
        double[] sumScore2 = new double[n];

        for (int t = 0; t < trials; t++) {
            int[] s = fullEval ? null : SampledCode.getSample(c, d, sampleSize);
            for (int i = 0; i < n; i++) {
                long rank = fullEval
                        ? expectedSize.calcExpectedRankFirst(canonical[i], c, d, totalCodes, feedbackFreq)
                        : expectedSize.calcExpectedRank(canonical[i], s, c, d, feedbackFreq);
                double score = rank / (double) normSize;
                sumScore[i] += score;
                sumScore2[i] += score * score;
            }
        }

        int bestIdx = 0, secondIdx = -1;
        for (int i = 1; i < n; i++) {
            if (sumScore[i] < sumScore[bestIdx]) {
                secondIdx = bestIdx;
                bestIdx = i;
            } else if (secondIdx == -1 || sumScore[i] < sumScore[secondIdx]) {
                secondIdx = i;
            }
        }

        double confidence;
        if (fullEval || secondIdx == -1) {
            confidence = 100.0;
        } else {
            double avg1   = sumScore[bestIdx] / trials;
            double avg2   = sumScore[secondIdx] / trials;
            double var1   = (sumScore2[bestIdx] / trials) - avg1 * avg1;
            double var2   = (sumScore2[secondIdx] / trials) - avg2 * avg2;
            double stdErr = Math.sqrt((var1 + var2) / trials);
            double z      = (avg2 - avg1) / stdErr;
            confidence = 100.0 * normalCDF(z);
        }

        return new Result(bestIdx, sumScore[bestIdx] / trials, confidence,
                          (long) n * normSize * trials, fullEval);
    }

    /** Approximation of the standard normal CDF using Horner's method (Abramowitz & Stegun 26.2.17). */
    private static double normalCDF(double z) {
        if (z < 0) return 1.0 - normalCDF(-z);
        double t = 1.0 / (1.0 + 0.2316419 * z);
        double poly = t * (0.319381530
                                   + t * (-0.356563782
                                                  + t * (1.781477937
                                                                 + t * (-1.821255978
                                                                                + t * 1.330274429))));
        double pdf = Math.exp(-0.5 * z * z) / Math.sqrt(2 * Math.PI);
        return 1.0 - pdf * poly;
    }

    record Result(int bestIdx, double avgScore, double confidence,
                  long totalEvals, boolean fullEval
    ) { }
}
