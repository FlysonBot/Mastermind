package org.mastermind;

/**
 * Lazy cache for generated code arrays, shared across classes.
 *
 * <p>Keyed by [c][d]; each entry is populated on first access.
 */
public class CodeCache {

    private static final int[][][] allValidCache  = new int[10][10][];
    private static final int[][][] canonicalCache = new int[10][10][];

    public static int[] getAllValid(int c, int d) {
        if (allValidCache[c][d] == null) allValidCache[c][d] = AllValidCode.generateAllCodes(c, d);
        return allValidCache[c][d];
    }

    public static int[] getCanonical(int c, int d) {
        if (canonicalCache[c][d] == null) canonicalCache[c][d] = CanonicalCode.enumerateCanonicalForms(c, d);
        return canonicalCache[c][d];
    }
}
