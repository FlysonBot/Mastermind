package org.mastermind.compute;

import org.mastermind.codes.ConvertCode;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 3, time = 1)
@Fork(3)
public class ExpectedSizeBenchmark {

    @Benchmark
    @OutputTimeUnit(TimeUnit.MICROSECONDS)
    public void benchmarkTest(BenchmarkState state, Blackhole blackhole) {
        long expectedSize = state.calcExpectedRank(BenchmarkState.ind(1123));
        blackhole.consume(expectedSize);
    }

    @Benchmark
    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    public void variedTest(BenchmarkState state, Blackhole blackhole) {
        for (int guessInd = 0; guessInd < state.total; guessInd++) {
            long expectedSize = state.calcExpectedRank(guessInd);
            blackhole.consume(expectedSize);
        }
    }

    @State(Scope.Thread)
    public static class BenchmarkState {
        static final int C = 6, D = 4;
        private final int          total           = (int) Math.pow(C, D); // 1296
        private final int[]        secretsInd;
        private final int[]        feedbackFreq    = new int[100];
        private final ExpectedSize expectedSizeObj = new ExpectedSize(D);

        public BenchmarkState() {
            secretsInd = new int[total];
            for (int i = 0; i < total; i++) secretsInd[i] = i;
        }

        static int ind(int code) { return ConvertCode.toIndex(C, D, code); }

        public long calcExpectedRank(int guessInd) {
            return expectedSizeObj.calcExpectedRank(guessInd, secretsInd, C, D, feedbackFreq);
        }
    }
}

/* Average Performance:
Benchmark                            Mode  Cnt   Score   Error  Units
ExpectedSizeBenchmark.benchmarkTest  avgt    9  25.656 ± 1.551  us/op
ExpectedSizeBenchmark.variedTest     avgt    9  32.383 ± 2.467  ms/op
 */