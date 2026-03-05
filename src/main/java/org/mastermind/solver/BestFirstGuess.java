package org.mastermind.solver;

import org.mastermind.codes.AllValidCode;
import org.mastermind.codes.CanonicalCode;
import org.mastermind.codes.ConvertCode;
import org.mastermind.codes.SampledCode;

/**
 * Provides the best first guess for any supported Mastermind configuration,
 * and a calibration tool that computes and prints the values to hardcode.
 * <p>
 * Use {@link #of(int, int)} at runtime. Run {@link #main(String[])} once to
 * regenerate the hardcoded values after algorithm changes.
 */
public class BestFirstGuess {

    // --- Calibration constants ---
    private static final int    TRIALS               = 100;
    private static final long   TARGET_EVALS         = 13_000_000L;
    private static final double CONFIDENCE_THRESHOLD = 99.0;
    private static final int    BUDGET_MULTIPLIER    = 2;

    // -------------------------------------------------------------------------
    // Calibration — run main() to recompute and regenerate the switch above
    // -------------------------------------------------------------------------

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

    private static Result evaluate(
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

    /**
     * Returns the best first guess and its true rank for a Mastermind game of c colors and d digits.
     *
     * @param c number of colors (2–9)
     * @param d number of digits (1–9)
     * @return long[2] where [0] = best first guess code (e.g. 1123), [1] = true rank (raw calcExpectedRank)
     * @throws IllegalArgumentException if c or d is out of the supported range
     */
    public static long[] of(int c, int d) {
        if (c < 2 || c > 9 || d < 1 || d > 9)
            throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);

        // d=1: single digit, all guesses equivalent — always guess 1
        if (d == 1) {
            int[] allSecrets = AllValidCode.generateAllCodes(c, 1);
            long rank = new ExpectedSize(1).calcExpectedRank(ConvertCode.toIndex(c, 1, 1), allSecrets, c, 1,
                                                             new int[100]);
            return new long[] { 1, rank };
        }

        return switch (c) {
            case 2 -> switch (d) {
                case 2 -> new long[] { 11, 6L };
                case 3 -> new long[] { 112, 16L };
                case 4 -> new long[] { 1112, 46L };
                case 5 -> new long[] { 11112, 148L };
                case 6 -> new long[] { 111112, 514L };
                case 7 -> new long[] { 1111122, 1752L };
                case 8 -> new long[] { 11111122, 5958L };
                case 9 -> new long[] { 111111122, 21250L };
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 3 -> switch (d) {
                case 2 -> new long[] { 12, 23L };
                case 3 -> new long[] { 112, 119L };
                case 4 -> new long[] { 1122, 775L };
                case 5 -> new long[] { 11123, 5099L };
                case 6 -> new long[] { 111123, 37271L };
                case 7 -> new long[] { 1111223, 289973L };
                case 8 -> new long[] { 11111223, 2234617L };
                case 9 -> new long[] { 111111223, 18004767L };
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 4 -> switch (d) {
                case 2 -> new long[] { 12, 70L };
                case 3 -> new long[] { 123, 690L };
                case 4 -> new long[] { 1123, 7892L };
                case 5 -> new long[] { 11223, 100950L };
                case 6 -> new long[] { 111223, 1318952L };
                case 7 -> new long[] { 1112223, 17732570L };
                case 8 -> new long[] { 11112223, 246242208L };
                case 9 -> new long[] { 111122223, 3424656050L };
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 5 -> switch (d) {
                case 2 -> new long[] { 12, 183L };
                case 3 -> new long[] { 123, 2751L };
                case 4 -> new long[] { 1123, 50807L };
                case 5 -> new long[] { 11223, 988703L };
                case 6 -> new long[] { 112233, 20472687L };
                case 7 -> new long[] { 1112223, 432675025L };
                case 8 -> new long[] { 11122233, 9432668521L };
                case 9 -> new long[] { 111122223, 207807845615L };
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 6 -> switch (d) {
                case 2 -> new long[] { 12, 422L };
                case 3 -> new long[] { 123, 8906L };
                case 4 -> new long[] { 1123, 240108L };
                case 5 -> new long[] { 11223, 6659862L };
                case 6 -> new long[] { 112233, 194108442L };
                case 7 -> new long[] { 1112233, 5987538014L };
                case 8 -> new long[] { 11122233, 185462657858L };
                case 9 -> new long[] { 111222333, 5820009319166L };
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 7 -> switch (d) {
                case 2 -> new long[] { 12, 871L };
                case 3 -> new long[] { 123, 24387L };
                case 4 -> new long[] { 1234, 882063L };
                case 5 -> new long[] { 11223, 34192827L };
                case 6 -> new long[] { 112233, 1334737119L };
                case 7 -> new long[] { 1112233, 56058606307L };
                case 8 -> new long[] { 11122233, 2362723139081L };
                case 9 -> new long[] { 111222333, 100244736768813L };
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 8 -> switch (d) {
                case 2 -> new long[] { 12, 1638L };
                case 3 -> new long[] { 123, 58866L };
                case 4 -> new long[] { 1234, 2724406L };
                case 5 -> new long[] { 11234, 140346626L };
                case 6 -> new long[] { 112233, 7211734938L };
                case 7 -> new long[] { 1122334, 386821286390L };
                case 8 -> new long[] { 11223344, 21165744470710L };
                case 9 -> new long[] { 111223344, 1201215086592578L };
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 9 -> switch (d) {
                case 2 -> new long[] { 12, 2855L };
                case 3 -> new long[] { 123, 128975L };
                case 4 -> new long[] { 1234, 7437615L };
                case 5 -> new long[] { 12345, 486776063L };
                case 6 -> new long[] { 112234, 32113088737L };
                case 7 -> new long[] { 1122334, 2148685524777L };
                case 8 -> new long[] { 11223344, 147476714738127L };
                case 9 -> new long[] { 111223344, 10597696978901189L };
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
        };
    }

    private record Result(int bestIdx, double avgScore, double confidence,
                          long totalEvals, boolean fullEval
    ) { }
}
