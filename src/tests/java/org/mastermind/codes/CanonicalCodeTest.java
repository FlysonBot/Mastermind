package org.mastermind.codes;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

class CanonicalCodeTest {

    @Nested
    @DisplayName("Calculate Canonical Count")
    class CanonicalCodeCount {
        @Test
        @DisplayName("Verify the user-provided example: c=6, d=9")
        void testPromptExample() {
            // Output should be 21147
            assertEquals(21147, CanonicalCode.countCanonicalForms(9, 9));
        }

        @ParameterizedTest
        @DisplayName("Small known values for Stirling sum")
        @CsvSource({
                "1, 1, 1",     // S(1,1) = 1
                "2, 3, 4",     // S(3,1) + S(3,2) = 1 + 3 = 4
                "3, 4, 14",    // S(4,1) + S(4,2) + S(4,3) = 1 + 7 + 6 = 14
                "1, 10, 1"     // S(n,1) is always 1
        })
        void testSmallValues(int c, int d, int expected) {
            assertEquals(expected, CanonicalCode.countCanonicalForms(c, d));
        }

        @Test
        @DisplayName("When c >= d, the result is the Bell number B_d")
        void testBellNumberIdentity() {
            // Bell numbers: B_3=5, B_5=52
            assertEquals(5, CanonicalCode.countCanonicalForms(3, 3));
            assertEquals(52, CanonicalCode.countCanonicalForms(10, 5));
        }

        @Test
        @DisplayName("Edge cases for zeros")
        void testZeroCases() {
            assertEquals(0, CanonicalCode.countCanonicalForms(0, 5), "Sum up to k=0 should be 0");
            assertEquals(0, CanonicalCode.countCanonicalForms(5, 0), "Stirling numbers for d=0 are 0");
        }

        @Test
        @DisplayName("Maximum safe value for 32-bit signed int")
        void testMaxIntSafety() {
            // B_15 is 1,382,958,545, which is < 2,147,483,647 (Max Int)
            int bell15 = 1382958545;
            assertEquals(bell15, CanonicalCode.countCanonicalForms(15, 15));
        }
    }

    @Nested
    @DisplayName("Enumerate Canonical Forms")
    class CanonicalCodeForms {

        /**
         * Helper to verify if an index is canonical.
         * Extracts digits left-to-right and checks no color is skipped.
         */
        private boolean isCanonicalInd(int ind, int c, int d) {
            int maxSeen = -1; // highest digit value seen so far (0-based)
            int place   = (int) Math.pow(c, d - 1);
            for (int pos = 0; pos < d; pos++) {
                int digitVal = ind / place; // 0..c-1
                ind %= place;
                place /= c;
                if (digitVal > maxSeen + 1) return false;
                if (digitVal > maxSeen) maxSeen = digitVal;
            }
            return true;
        }

        @Test
        @DisplayName("Verify array size matches Stirling Sum for (9, 9)")
        void testArraySize() {
            int   c            = 9;
            int   d            = 9;
            int   expectedSize = CanonicalCode.countCanonicalForms(c, d); // 21147
            int[] results      = CanonicalCode.enumerateCanonicalForms(c, d);

            assertEquals(expectedSize, results.length);
            assertEquals(21147, results.length);
        }

        @Test
        @DisplayName("Verify specific canonical form indices for small c, d")
        void testSmallEnumeration() {
            // For c=2, d=3, canonical forms are: 111, 112, 121, 122
            // As indices (c=2): 0, 1, 2, 3
            int[] expected = { 0, 1, 2, 3 };
            int[] actual   = CanonicalCode.enumerateCanonicalForms(2, 3);

            assertArrayEquals(expected, actual);
        }

        @Test
        @DisplayName("Verify Rule 1: All codes must start with color 1 (digitVal 0)")
        void testStartsWithOne() {
            int   c         = 6, d = 4;
            int   threshold = (int) Math.pow(c, d - 1); // indices with leading digitVal 0 are < c^(d-1)
            int[] results   = CanonicalCode.enumerateCanonicalForms(c, d);
            for (int ind : results) {
                assertTrue(ind < threshold, "Index " + ind + " does not start with digitVal 0 (color 1)");
            }
        }

        @Test
        @DisplayName("Verify Rule 2: No skipping colors (Canonical check)")
        void testNoSkippedColors() {
            int   c       = 6, d = 5;
            int[] results = CanonicalCode.enumerateCanonicalForms(c, d);
            for (int ind : results) {
                assertTrue(isCanonicalInd(ind, c, d), "Index " + ind + " violates canonical rules");
            }
        }

        @Test
        @DisplayName("Edge Case: c=1")
        void testSingleColor() {
            // If only 1 color, every digit is 0 → index 0
            int[] results = CanonicalCode.enumerateCanonicalForms(1, 4);
            assertEquals(1, results.length);
            assertEquals(0, results[0]);
        }

        @Test
        @DisplayName("Edge Case: d=1")
        void testSingleDigit() {
            // If length is 1, only color 1 (digitVal 0) is possible → index 0
            int[] results = CanonicalCode.enumerateCanonicalForms(6, 1);
            assertEquals(1, results.length);
            assertEquals(0, results[0]);
        }
    }
}
