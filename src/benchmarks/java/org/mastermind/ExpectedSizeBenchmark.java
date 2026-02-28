package org.mastermind;

import org.mastermind.codes.AllValidCode;
import org.mastermind.solver.ExpectedSize;
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
        long expectedSize = state.calcExpectedRank(1123);
        blackhole.consume(expectedSize);
    }

    @Benchmark
    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    public void variedTest(BenchmarkState state, Blackhole blackhole) {
        for (int guess : state.secrets) {
            long expectedSize = state.calcExpectedRank(guess);
            blackhole.consume(expectedSize);
        }
    }

    @State(Scope.Thread)
    public static class BenchmarkState {
        private final int[]        secrets         = AllValidCode.generateAllCodes(6, 4);
        private final int[]        feedbackFreq    = new int[100];
        private final ExpectedSize expectedSizeObj = new ExpectedSize(4);

        public long calcExpectedRank(int guess) {
            return expectedSizeObj.calcExpectedRank(guess, secrets, 6, 4, feedbackFreq);
        }
    }
}

/* Benchmark Average:
Benchmark                            Mode  Cnt   Score   Error  Units
ExpectedSizeBenchmark.benchmarkTest  avgt    9  25.096 ± 1.178  us/op
ExpectedSizeBenchmark.variedTest     avgt    9  34.095 ± 0.792  ms/op
 */