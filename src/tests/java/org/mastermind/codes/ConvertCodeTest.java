package org.mastermind.codes;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

class ConvertCodeTest {

    @Nested
    @DisplayName("toIndex")
    class ToIndex {

        @ParameterizedTest
        @DisplayName("Boundary codes for c=6, d=4")
        @CsvSource({
                "6, 4, 1111, 0",
                "6, 4, 1112, 1",
                "6, 4, 6666, 1295",
        })
        void testBoundaries(int c, int d, int code, int expected) {
            assertEquals(expected, ConvertCode.toIndex(c, d, code));
        }

        @Test
        @DisplayName("Mid-range code 1234 for c=6, d=4")
        void testMidRange() {
            // 1234: digits (left=most-sig) 1,2,3,4 → positions 3,2,1,0
            // index = (1-1)*6^3 + (2-1)*6^2 + (3-1)*6^1 + (4-1)*6^0
            //       = 0*216 + 1*36 + 2*6 + 3*1 = 0 + 36 + 12 + 3 = 51
            assertEquals(51, ConvertCode.toIndex(6, 4, 1234));
        }

        @Test
        @DisplayName("Single-digit code for c=9, d=1")
        void testSingleDigit() {
            assertEquals(0, ConvertCode.toIndex(9, 1, 1));
            assertEquals(8, ConvertCode.toIndex(9, 1, 9));
        }
    }

    @Nested
    @DisplayName("toCode")
    class ToCode {

        @ParameterizedTest
        @DisplayName("Boundary indices for c=6, d=4")
        @CsvSource({
                "6, 4, 0, 1111",
                "6, 4, 1, 1112",
                "6, 4, 1295, 6666",
        })
        void testBoundaries(int c, int d, int index, int expected) {
            assertEquals(expected, ConvertCode.toCode(c, d, index));
        }

        @Test
        @DisplayName("Index 51 for c=6, d=4")
        void testMidRange() {
            assertEquals(1234, ConvertCode.toCode(6, 4, 51));
        }

        @Test
        @DisplayName("Single-digit index for c=9, d=1")
        void testSingleDigit() {
            assertEquals(1, ConvertCode.toCode(9, 1, 0));
            assertEquals(9, ConvertCode.toCode(9, 1, 8));
        }
    }

    @Nested
    @DisplayName("Round-trip")
    class RoundTrip {

        @Test
        @DisplayName("toCode(toIndex(code)) == code for c=6, d=4")
        void testCodeToIndexToCode() {
            int c     = 6, d = 4;
            int total = (int) Math.pow(c, d);
            for (int idx = 0; idx < total; idx++) {
                int code = ConvertCode.toCode(c, d, idx);
                assertEquals(idx, ConvertCode.toIndex(c, d, code),
                             "Round-trip failed for index " + idx);
            }
        }

        @Test
        @DisplayName("toIndex(toCode(idx)) == idx for c=4, d=3")
        void testIndexToCodeToIndex() {
            int c     = 4, d = 3;
            int total = (int) Math.pow(c, d);
            for (int idx = 0; idx < total; idx++) {
                assertEquals(idx, ConvertCode.toIndex(c, d, ConvertCode.toCode(c, d, idx)),
                             "Round-trip failed for index " + idx);
            }
        }
    }
}
