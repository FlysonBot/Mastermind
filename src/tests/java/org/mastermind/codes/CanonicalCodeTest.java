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
        @DisplayName("c=9, d=9 yields 30 integer partitions")
        void testMainCase() {
            assertEquals(30, CanonicalCode.countCanonicalForms(9, 9));
        }

        @ParameterizedTest
        @DisplayName("Small known values (integer partitions of d with at most c parts)")
        @CsvSource({
                "1, 1, 1",   // {1}
                "2, 3, 2",   // {3}, {2,1}
                "3, 4, 4",   // {4}, {3,1}, {2,2}, {2,1,1}
                "1, 10, 1"   // only {10}
        })
        void testSmallValues(int c, int d, int expected) {
            assertEquals(expected, CanonicalCode.countCanonicalForms(c, d));
        }

        @Test
        @DisplayName("When c >= d, the result is p(d), the partition number")
        void testPartitionNumberIdentity() {
            // p(3)=3, p(5)=7
            assertEquals(3, CanonicalCode.countCanonicalForms(3, 3));
            assertEquals(7, CanonicalCode.countCanonicalForms(10, 5));
        }

        @Test
        @DisplayName("Edge cases for zeros")
        void testZeroCases() {
            assertEquals(0, CanonicalCode.countCanonicalForms(0, 5));
            assertEquals(0, CanonicalCode.countCanonicalForms(5, 0));
        }

        @Test
        @DisplayName("Maximum safe value for 32-bit signed int")
        void testMaxIntSafety() {
            // p(15) = 176, well within int range
            assertEquals(176, CanonicalCode.countCanonicalForms(15, 15));
        }
    }

    @Nested
    @DisplayName("Enumerate Canonical Forms")
    class CanonicalCodeForms {

        @Test
        @DisplayName("Array size matches countCanonicalForms for (9, 9)")
        void testArraySize() {
            int[] results = CanonicalCode.enumerateCanonicalForms(9, 9);
            assertEquals(30, results.length);
        }

        @Test
        @DisplayName("Specific indices for c=2, d=3")
        void testSmallEnumeration() {
            // Partitions of 3 with <= 2 parts: {3} and {2,1}
            // {3}   → color 0 fills all 3 positions → index 0 (000 in base 2)
            // {2,1} → color 0 fills pos 0,1; color 1 fills pos 2 → 0*4 + 0*2 + 1*1 = 1
            int[] expected = { 0, 1 };
            assertArrayEquals(expected, CanonicalCode.enumerateCanonicalForms(2, 3));
        }

        @Test
        @DisplayName("Edge Case: c=1")
        void testSingleColor() {
            int[] results = CanonicalCode.enumerateCanonicalForms(1, 4);
            assertEquals(1, results.length);
            assertEquals(0, results[0]);
        }

        @Test
        @DisplayName("Edge Case: d=1")
        void testSingleDigit() {
            int[] results = CanonicalCode.enumerateCanonicalForms(6, 1);
            assertEquals(1, results.length);
            assertEquals(0, results[0]);
        }
    }
}
