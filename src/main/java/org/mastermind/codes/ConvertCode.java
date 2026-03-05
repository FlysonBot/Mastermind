package org.mastermind.codes;

/**
 * Converts between Mastermind codes (as ints, e.g. 1234) and their index
 * in the array produced by AllValidCode.generateAllCodes(c, d).
 * <p>
 * Encoding: index is a base-c number where each "digit" runs 0..c-1.
 * Position 0 is the rightmost (least significant) digit of the code.
 * Code digit value = (index / c^pos) % c + 1.
 * <p>
 * Examples (c=6, d=4):
 * index 0    → code 1111
 * index 1    → code 1112
 * index 1295 → code 6666
 */
public class ConvertCode {

    /**
     * Convert a code int to its index in the AllValidCode array.
     *
     * @param c    number of colors
     * @param d    number of digits
     * @param code the code as an int (e.g. 1234)
     * @return the 0-based index of this code
     */
    public static int toIndex(int c, int d, int code) {
        int index = 0;
        int place = 1; // c^pos
        for (int pos = 0; pos < d; pos++) {
            int digit = (code % 10) - 1; // extract rightmost decimal digit, map 1..c → 0..c-1
            index += digit * place;
            code /= 10;
            place *= c;
        }
        return index;
    }

    /**
     * Convert a 0-based index to the corresponding code int.
     *
     * @param c     number of colors
     * @param d     number of digits
     * @param index the 0-based index
     * @return the code as an int (e.g. 1234)
     */
    public static int toCode(int c, int d, int index) {
        int code  = 0;
        int pow10 = 1; // 10^pos
        for (int pos = 0; pos < d; pos++) {
            int digit = (index % c) + 1; // map 0..c-1 → 1..c
            code += digit * pow10;
            index /= c;
            pow10 *= 10;
        }
        return code;
    }
}
