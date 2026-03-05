package org.mastermind.codes;

/**
 * Canonical forms are one representative code per symmetry equivalence class,
 * used to reduce the first-guess search space.
 *
 * <p>At turn 0, both color-relabeling symmetry and position-permutation symmetry
 * are intact. Two codes are equivalent if one can be obtained from the other by
 * any permutation of colors and any permutation of digit positions. The equivalence
 * classes are exactly the integer partitions of d into at most c parts — the
 * multiset of color frequencies, or "bucket." For c=9, d=9 this gives just 30
 * canonical forms, down from 387,420,489 total codes.
 */
public class CanonicalCode {
    /**
     * Count the number of canonical forms (integer partitions of d with at most c parts).
     *
     * @param c number of colors (<= 9)
     * @param d number of digits (<= 9)
     * @return number of canonical forms
     */
    public static int countCanonicalForms(int c, int d) {
        if (c <= 0 || d <= 0) return 0;
        // By conjugate partition identity: partitions of d into at most c parts
        // = partitions of d with the largest part <= c.
        // dp[i][j] = number of partitions of i with the largest part <= j.
        int[][] dp = new int[d + 1][c + 1];
        for (int i = 0; i <= d; i++) dp[i][0] = (i == 0) ? 1 : 0;
        for (int maxPart = 1; maxPart <= c; maxPart++) {
            for (int i = 0; i <= d; i++) {
                dp[i][maxPart] = dp[i][maxPart - 1];
                if (i >= maxPart) dp[i][maxPart] += dp[i - maxPart][maxPart];
            }
        }
        return dp[d][c];
    }

    /**
     * Enumerate all canonical forms as code indices.
     * The representative for each partition is the lex-smallest index in its
     * equivalence class: the most-frequent color gets digit value 0 and occupies
     * the leftmost positions, the next color gets digit value 1, and so on.
     *
     * @param c number of colors (<= 9)
     * @param d number of digits (<= 9)
     * @return array of canonical indices, one per integer partition of d with <= c parts
     */
    public static int[] enumerateCanonicalForms(int c, int d) {
        int[] results = new int[countCanonicalForms(c, d)];
        int[] index   = { 0 };
        int[] place   = new int[d];
        place[d - 1] = 1;
        for (int i = d - 2; i >= 0; i--) place[i] = place[i + 1] * c;

        int[] freq = new int[c];
        generateFrequencies(results, index, freq, 0, d, d, place);
        return results;
    }

    private static void generateFrequencies(
            int[] results, int[] index, int[] freq, int color, int remaining, int maxFreq, int[] place
    ) {
        if (remaining == 0) {
            results[index[0]++] = buildIndex(freq, color, place);
            return;
        }
        if (color == freq.length) return;

        int limit = Math.min(maxFreq, remaining);
        for (int f = limit; f >= 1; f--) {
            freq[color] = f;
            generateFrequencies(results, index, freq, color + 1, remaining - f, f, place);
        }
    }

    private static int buildIndex(int[] freq, int numColors, int[] place) {
        // Maps a partition (color frequency array) to its lex-smallest representative index.
        // Color 0 gets the highest frequency and occupies the leftmost positions,
        // color 1 gets the next frequency, and so on. This ensures all codes with the
        // same partition map to the same canonical representative.
        int ind = 0;
        int pos = 0;
        for (int color = 0; color < numColors; color++) {
            for (int f = 0; f < freq[color]; f++) {
                ind += color * place[pos++];
            }
        }
        return ind;
    }
}
