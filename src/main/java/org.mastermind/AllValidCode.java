package org.mastermind;

/**
 * A game of Mastermind has 2 parameters, c (number of colors)
 * and d (number of digits). A code is a valid Mastermind code
 * if it has exactly d digits, and uses values between 1 and c
 * inclusively for each digit.
 */
public class AllValidCode {
    /**
     * Generate all valid Mastermind code for a game.
     *
     * @param c     number of colors (<= 9)
     * @param d     number of digits (<= 9)
     * @return      Array of all valid Mastermind code
     */
    public static int[] generateAllCodes(int c, int d) {
        // Total number of codes = c^d (e.g. 6 colors, 4 pegs = 1296 codes)
        int total = 1;
        for (int i = 0; i < d; i++) total *= c;

        int[] codes = new int[total];

        // digits[] tracks the current code as individual digits (0-indexed internally).
        // digits[0] is the RIGHTMOST (least significant) digit,
        // digits[d-1] is the LEFTMOST (most significant) digit.
        // Internally digits run 0..c-1; we add 1 when building the int so output is 1..c.
        int[] digits = new int[d];

        // Precompute positional powers of 10 matching the digits[] layout:
        // pow10[0] = 1    (rightmost / least significant)
        // pow10[1] = 10
        // pow10[2] = 100
        // pow10[d-1]      (leftmost / most significant)
        // e.g. d=4: pow10 = [1, 10, 100, 1000]
        int[] pow10 = new int[d];
        pow10[0] = 1;
        for (int i = 1; i < d; i++) {
            pow10[i] = pow10[i - 1] * 10;
        }

        // The starting code is all 1s (e.g. d=4 → 1111).
        // Since digits[] is initialized to all 0s (representing digit value 1),
        // the base code is just the sum of all positional powers of 10.
        int code = 0;
        for (int i = 0; i < d; i++) code += pow10[i];

        for (int i = 0; i < total; i++) {
            // Store the current code before incrementing
            codes[i] = code;

            // --- Odometer-style increment ---
            // We tick the rightmost digit (index 0) up by 1, exactly like an odometer.
            // If a digit exceeds c, it wraps back to 1 and carries over to the next
            // digit to the left (index + 1).
            int pos = 0; // start at the least significant (rightmost) digit
            while (pos < d) {
                digits[pos]++;        // increment this digit
                code += pow10[pos];   // reflect the +1 in the integer representation

                if (digits[pos] < c) {
                    // No carry needed — the digit is still within range [1..c].
                    break;
                } else {
                    // This digit has exceeded c, so wrap it back to 1.
                    // In terms of the integer: we added 1 just above, but we need
                    // the digit to go from c back to 1, a net change of (1 - c).
                    // We already added pow10[pos], so subtract c * pow10[pos]
                    // to get the net effect of -(c-1) * pow10[pos].
                    // e.g. c=6, pos=0 (units place, pow10=1): digit went 6→1,
                    //   code already +1, now -6, net = -5 ✓ (6→1 is -5 in value)
                    code -= c * pow10[pos];
                    digits[pos] = 0;  // reset internal digit to 0 (represents value 1)

                    pos++;            // carry: move left to the next digit (higher index)
                }
            }
            // When the while loop exits without breaking (pos >= d), all digits
            // have wrapped around — we've generated every code and are done.
        }

        return codes;
    }
}