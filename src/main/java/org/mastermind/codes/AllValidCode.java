package org.mastermind.codes;

/**
 * A game of Mastermind has 2 parameters, c (number of colors)
 * and d (number of digits). A code is a valid Mastermind code
 * if it has exactly d digits, and uses values between 1 and c
 * inclusively for each digit.
 */
public final class AllValidCode {
    /**
     * Generate all valid Mastermind code indices for a game.
     *
     * @param c number of colors (<= 9)
     * @param d number of digits (<= 9)
     * @return Array of all valid code indices in [0, c^d)
     */
    public static int[] generateAllCodes(int c, int d) {
        int   total = (int) Math.pow(c, d);
        int[] ind   = new int[total];
        for (int i = 0; i < total; i++) ind[i] = i;
        return ind;
    }
}
