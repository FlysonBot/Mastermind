package org.mastermind;

import org.mastermind.codes.AllValidCode;
import org.mastermind.solver.ExpectedSize;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 3, time = 1)
@Fork(5)
public class ExpectedSizeBenchmark {

    @Benchmark
    public void benchmarkTest(BenchmarkState state, Blackhole blackhole) {
        long expectedSize = state.calcExpectedRank(1123);
        blackhole.consume(expectedSize);
    }

    @State(Scope.Thread)
    public static class BenchmarkState {
        private final int[]        secrets         = AllValidCode.generateAllCodes(6, 4);
        private final int[]        feedbackFreq    = new int[100];
        private final ExpectedSize expectedSizeObj = new ExpectedSize(4);

        public long calcExpectedRank(int guess) {
            return expectedSizeObj.calcExpectedRank(guess, secrets, 4, feedbackFreq);
        }
    }
}

/* Benchmark Average:
Benchmark                            Mode  Cnt   Score   Error  Units
ExpectedSizeBenchmark.benchmarkTest  avgt   15  22.821 ± 0.313  us/op
 */