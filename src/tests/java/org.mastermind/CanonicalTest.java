package org.mastermind;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class CanonicalTest {

    @Nested
    @DisplayName("Calculate Canonical Count")
    class CanonicalCount {
        @Test
        @DisplayName("Verify the user-provided example: c=6, d=9")
        void testPromptExample() {
            // Output should be 21147
            assertEquals(21147, Canonical.countCanonicalForms(9, 9));
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
            assertEquals(expected, Canonical.countCanonicalForms(c, d));
        }

        @Test
        @DisplayName("When c >= d, the result is the Bell number B_d")
        void testBellNumberIdentity() {
            // Bell numbers: B_3=5, B_5=52
            assertEquals(5, Canonical.countCanonicalForms(3, 3));
            assertEquals(52, Canonical.countCanonicalForms(10, 5));
        }

        @Test
        @DisplayName("Edge cases for zeros")
        void testZeroCases() {
            assertEquals(0, Canonical.countCanonicalForms(0, 5), "Sum up to k=0 should be 0");
            assertEquals(0, Canonical.countCanonicalForms(5, 0), "Stirling numbers for d=0 are 0");
        }

        @Test
        @DisplayName("Maximum safe value for 32-bit signed int")
        void testMaxIntSafety() {
            // B_15 is 1,382,958,545, which is < 2,147,483,647 (Max Int)
            int bell15 = 1382958545;
            assertEquals(bell15, Canonical.countCanonicalForms(15, 15));
        }
    }

    @Nested
    @DisplayName("Enumerate Canonical Forms")
    class CanonicalForms{
        /**
         * Helper to verify if a number is mathematically canonical.
         * New colors must be the smallest available integer.
         */
        private boolean isCanonical(int code, int d) {
            int maxSeen = 0;
            int divisor = (int) Math.pow(10, d - 1);

            while (divisor > 0) {
                int digit = code / divisor; // Get the leftmost digit

                if (digit > maxSeen + 1) return false;
                if (digit > maxSeen) maxSeen = digit;

                code %= divisor;    // Remove the leftmost digit
                divisor /= 10;      // Move to the next place value
            }
            return true;
        }

        @Test
        @DisplayName("Verify array size matches Stirling Sum for (6, 9)")
        void testArraySize() {
            int c = 9;
            int d = 9;
            int expectedSize = Canonical.countCanonicalForms(c, d); // 21147
            int[] results = Canonical.enumerateCanonicalForms(c, d);

            assertEquals(expectedSize, results.length);
            assertEquals(21147, results.length);
        }

        @Test
        @DisplayName("Verify specific canonical forms for small c, d")
        void testSmallEnumeration() {
            // For c=2, d=3, canonical forms should be:
            // 111 (uses 1 color)
            // 112 (uses 2 colors)
            // 121 (uses 2 colors)
            // 122 (uses 2 colors)
            int[] expected = {111, 112, 121, 122};
            int[] actual = Canonical.enumerateCanonicalForms(2, 3);

            assertArrayEquals(expected, actual, "Should generate exactly 111, 112, 121, 122");
        }

        @Test
        @DisplayName("Verify Rule 1: All codes must start with 1")
        void testStartsWithOne() {
            int[] results = Canonical.enumerateCanonicalForms(6, 4);
            for (int code : results) {
                // A 4-digit number starting with 1 is between 1000 and 1999
                assertTrue(code >= 1000 && code <= 1999, "Code " + code + " must start with 1");
            }
        }

        @Test
        @DisplayName("Verify Rule 2: No skipping colors (Canonical check)")
        void testNoSkippedColors() {
            int[] results = Canonical.enumerateCanonicalForms(6, 5);
            for (int code : results) {
                assertTrue(isCanonical(code, 5), "Code " + code + " violates canonical rules");
            }
        }

        @Test
        @DisplayName("Edge Case: c=1")
        void testSingleColor() {
            // If only 1 color is allowed, every digit must be 1
            int[] results = Canonical.enumerateCanonicalForms(1, 4);
            assertEquals(1, results.length);
            assertEquals(1111, results[0]);
        }

        @Test
        @DisplayName("Edge Case: d=1")
        void testSingleDigit() {
            // If length is 1, only '1' is possible
            int[] results = Canonical.enumerateCanonicalForms(6, 1);
            assertEquals(1, results.length);
            assertEquals(1, results[0]);
        }
    }
}