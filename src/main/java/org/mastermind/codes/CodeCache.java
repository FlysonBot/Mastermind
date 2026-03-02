package org.mastermind.codes;

/**
 * Lazy cache for generated code arrays, shared across classes.
 *
 * <p>Keyed by [c][d]; each entry is populated on first access.
 */
public class CodeCache {

    private static final int[][][] allValidCache = new int[10][10][];

    public static int[] getAllValid(int c, int d) {
        if (allValidCache[c][d] == null) allValidCache[c][d] = AllValidCode.generateAllCodes(c, d);
        return allValidCache[c][d];
    }

}
