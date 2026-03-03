package org.mastermind.codes;

/**
 * Canonical forms refer to a specific subset of all Mastermind code
 * that starts with 1, digit ordered from small to large starting
 * from the left, and the highest value digit equals to the number
 * of colors used in the code. This is helpful at the beginning of
 * the game before any guesses are made, where color and positional
 * symmetry remain unbroken, allowing for a reduced search space to
 * find the best first guess.
 */
public class CanonicalCode {
    /**
     * Calculate the number of Canonical forms in a Mastermind game using
     * Stirling number of the second kind.
     *
     * @param c number of colors (<= 9)
     * @param d number of digits (<= 9)
     * @return Number of Canonical form in Mastermind
     */
    public static int countCanonicalForms(int c, int d) {
        // Edge cases for empty sets or partitions
        int maxK = Math.min(c, d);
        if (maxK <= 0) return 0;

        // 1D DP array to save memory
        int[] dp = new int[maxK + 1];

        // Base case: S(0, 0) = 1
        dp[0] = 1;

        for (int i = 1; i <= d; i++) {
            // Update the row backwards to avoid overwriting values needed
            // for the current calculation: S(n,k) = k*S(n-1,k) + S(n-1,k-1)
            for (int j = Math.min(i, maxK); j >= 1; j--) {
                dp[j] = j * dp[j] + dp[j - 1];
            }
            // S(i, 0) is 0 for all i > 0
            dp[0] = 0;
        }

        // Sum the results S(d, 1) through S(d, maxK)
        int sum = 0;
        for (int k = 1; k <= maxK; k++) {
            sum += dp[k];
        }
        return sum;
    }

    /**
     * Enumerate all Canonical forms in a Mastermind game as code indices.
     *
     * @param c number of colors (<= 9)
     * @param d number of digits (<= 9)
     * @return Array of indices (0-based, base-c encoding) of all Canonical forms
     */
    public static int[] enumerateCanonicalForms(int c, int d) {

        // 1. Calculate the exact size needed using our Stirling Sum logic
        int[] results = new int[countCanonicalForms(c, d)];

        // 2. Use a tiny wrapper array for the index to pass by reference in recursion
        int[] index = { 0 };

        // 3. Precompute positional powers: place[pos] = c^(d-1-pos) for left-to-right building
        int[] place = new int[d];
        place[d - 1] = 1;
        for (int i = d - 2; i >= 0; i--) place[i] = place[i + 1] * c;

        // 4. Start recursion
        backtrack(results, index, 0, 0, 0, c, d, place);

        return results;
    }

    private static void backtrack(
            int[] results, int[] index, int currentInd, int pos, int maxColorUsed, int c, int d, int[] place) {
        // Base case: Code is complete
        if (pos == d) {
            results[index[0]++] = currentInd;
            return;
        }

        // Rule 1 & 2: Try existing colors (digit values 0..maxColorUsed-1 in index encoding)
        for (int digitVal = 0; digitVal < maxColorUsed; digitVal++) {
            backtrack(results, index, currentInd + digitVal * place[pos], pos + 1, maxColorUsed, c, d, place);
        }

        // Rule 3: Try exactly one "new" color if limit c isn't reached (digit value maxColorUsed)
        if (maxColorUsed < c) {
            backtrack(results, index, currentInd + maxColorUsed * place[pos], pos + 1, maxColorUsed + 1, c, d, place);
        }
    }
}
