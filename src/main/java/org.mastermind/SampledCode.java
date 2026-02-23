package org.mastermind;

import java.util.Random;

public class SampledCode {

    public static int[] getSample(int c, int d, int sampleSize) {
        Random random = new Random();
        int[] sample = new int[sampleSize];

        for (int i = 0; i < sampleSize; i++) {
            int code = 0;
            for (int digit = 0; digit < d; digit++) {
                int color = random.nextInt(c) + 1; // colors 1..c
                code = code * 10 + color;
            }
            sample[i] = code;
        }

        return sample;
    }

    public static int calcSampleSize(int feedbackSize) { return (int) (feedbackSize * Math.pow(1.96 / 0.05, 2)); }
}
