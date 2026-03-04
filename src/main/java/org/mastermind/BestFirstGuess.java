package org.mastermind;

import org.mastermind.codes.AllValidCode;
import org.mastermind.codes.CanonicalCode;
import org.mastermind.codes.ConvertCode;
import org.mastermind.codes.SampledCode;
import org.mastermind.solver.ExpectedSize;

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

    /**
     * Returns the best first guess code for a Mastermind game of c colors and d digits.
     *
     * @param c number of colors (2–9)
     * @param d number of digits (1–9)
     * @return best first guess as a code int (e.g. 1123)
     * @throws IllegalArgumentException if c or d is out of the supported range
     */
    public static int of(int c, int d) {
        if (c < 2 || c > 9 || d < 1 || d > 9)
            throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);

        // d=1: single digit, all guesses equivalent — always guess 1
        if (d == 1) return 1;

        return switch (c) {
            case 2 -> switch (d) {
                case 2 -> 11;
                case 3 -> 112;
                case 4 -> 1112;
                case 5 -> 11112;
                case 6 -> 111112;
                case 7 -> 1111122;
                case 8 -> 11111122;
                case 9 -> 111111122;
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 3 -> switch (d) {
                case 2 -> 12;
                case 3 -> 112;
                case 4 -> 1122;
                case 5 -> 11123;
                case 6 -> 111123;
                case 7 -> 1111223;
                case 8 -> 11111223;
                case 9 -> 111111223;
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 4 -> switch (d) {
                case 2 -> 12;
                case 3 -> 123;
                case 4 -> 1123;
                case 5 -> 11223;
                case 6 -> 111223;
                case 7 -> 1112223;
                case 8 -> 11112223;
                case 9 -> 111122223;
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 5 -> switch (d) {
                case 2 -> 12;
                case 3 -> 123;
                case 4 -> 1123;
                case 5 -> 11223;
                case 6 -> 112233;
                case 7 -> 1112223;
                case 8 -> 11122233;
                case 9 -> 111122223;
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 6 -> switch (d) {
                case 2 -> 12;
                case 3 -> 123;
                case 4 -> 1123;
                case 5 -> 11223;
                case 6 -> 112233;
                case 7 -> 1112233;
                case 8 -> 11122233;
                case 9 -> 111222333;
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 7 -> switch (d) {
                case 2 -> 12;
                case 3 -> 123;
                case 4 -> 1234;
                case 5 -> 11223;
                case 6 -> 112233;
                case 7 -> 1112233;
                case 8 -> 11122233;
                case 9 -> 111222333;
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 8 -> switch (d) {
                case 2 -> 12;
                case 3 -> 123;
                case 4 -> 1234;
                case 5 -> 11234;
                case 6 -> 112233;
                case 7 -> 1122334;
                case 8 -> 11223344;
                case 9 -> 111223344;
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            case 9 -> switch (d) {
                case 2 -> 12;
                case 3 -> 123;
                case 4 -> 1234;
                case 5 -> 12345;
                case 6 -> 112234;
                case 7 -> 1122334;
                case 8 -> 11223344;
                case 9 -> 111223344;
                default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
            };
            default -> throw new IllegalArgumentException("Unsupported game size: c=" + c + ", d=" + d);
        };
    }

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

        // Print switch snippet
        System.out.println("\n// --- copy below into of(int c, int d) ---");
        for (int c = 2; c <= 9; c++) {
            System.out.printf("            case %d -> switch (d) {%n", c);
            for (int d = 2; d <= 9; d++) {
                System.out.printf("                case %d -> %d;%n", d, bestCode[c][d]);
            }
            System.out.printf("                default -> throw new IllegalArgumentException(\"Unsupported game size: c=\" + c + \", d=\" + d);%n");
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
        int[]   allSecrets = fullEval ? AllValidCode.generateAllCodes(c, d) : null;
        int     normSize   = fullEval ? totalCodes : sampleSize;
        int     trials     = fullEval ? 1 : TRIALS;

        double[] sumScore  = new double[n];
        double[] sumScore2 = new double[n];

        for (int t = 0; t < trials; t++) {
            int[] s = fullEval ? allSecrets : SampledCode.getSample(c, d, sampleSize);
            for (int i = 0; i < n; i++) {
                double score = expectedSize.calcExpectedRank(canonical[i], s, c, d, feedbackFreq)
                        / (double) normSize;
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

    private record Result(int bestIdx, double avgScore, double confidence,
                          long totalEvals, boolean fullEval
    ) { }
}
