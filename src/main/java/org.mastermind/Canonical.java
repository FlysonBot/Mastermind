package org.mastermind;

public class Canonical {
    /**
     * Calculates the sum of Stirling numbers of the second kind S(d, k)
     * for k from 1 to min(c, d).
     * Safe for d up to 15 (B_15 fits in an int; B_16 requires a long).
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
     * Enumerates all canonical Mastermind codes as a primitive int array.
     */
    public static int[] enumerateCanonicalForms(int c, int d) {
        if (c <= 0 || d <= 0) return new int[0];

        // 1. Calculate the exact size needed using our Stirling Sum logic
        int totalSize = countCanonicalForms(c, d);
        int[] results = new int[totalSize];

        // 2. Use a tiny wrapper array for the index to pass by reference in recursion
        int[] index = {0};

        // 3. Start recursion
        backtrack(results, index, 0, 0, 0, c, d);

        return results;
    }

    private static void backtrack(int[] results, int[] index, int currentNum, int pos, int maxColorUsed, int c, int d) {
        // Base case: Code is complete
        if (pos == d) {
            results[index[0]++] = currentNum;
            return;
        }

        // Rule 1 & 2: Try existing colors
        for (int color = 1; color <= maxColorUsed; color++) {
            backtrack(results, index, (currentNum * 10) + color, pos + 1, maxColorUsed, c, d);
        }

        // Rule 3: Try exactly one "new" color if limit c isn't reached
        if (maxColorUsed < c) {
            int nextColor = maxColorUsed + 1;
            backtrack(results, index, (currentNum * 10) + nextColor, pos + 1, nextColor, c, d);
        }
    }
}
