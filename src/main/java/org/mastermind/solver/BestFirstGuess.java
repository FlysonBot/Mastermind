package org.mastermind.solver;

import org.mastermind.codes.AllValidCode;
import org.mastermind.codes.ConvertCode;
import org.mastermind.compute.ExpectedSize;

/**
 * Provides the best first guess for any supported Mastermind configuration.
 * <p>
 * Use {@link #of(int, int)} at runtime. Run {@link BestFirstGuessCalculator#main(String[])} once to
 * regenerate the hardcoded values after algorithm changes.
 */
public class BestFirstGuess {

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

        // To regenerate this table, run BestFirstGuessCalculator.main()
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
}
