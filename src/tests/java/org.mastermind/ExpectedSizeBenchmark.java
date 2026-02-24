package org.mastermind;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 3, time = 1)
@Fork(5)
public class ExpectedSizeBenchmark {

    // 1. STATE CLASS (nested static class)
    @State(Scope.Thread)
    public static class BenchmarkState {
        private final int[] secrets = AllValidCode.generateAllCodes(6, 4);
        private final int[] feedbackFreq = new int[100];
        private final ExpectedSize expectedSizeObj = new ExpectedSize(4);
        public float calcExpectedSize(int guess) {
            return expectedSizeObj.calcExpectedSize(guess, secrets, 4, 1296, feedbackFreq);
        }
    }

    // 2. BENCHMARK METHOD
    @Benchmark
    public void benchmarkTest(BenchmarkState state, Blackhole blackhole) {
        float expectedSize = state.calcExpectedSize(1123);
        blackhole.consume(expectedSize);
    }
}

/* Benchmark Average:
Benchmark                            Mode  Cnt   Score   Error  Units
ExpectedSizeBenchmark.benchmarkTest  avgt   15  22.821 ± 0.313  us/op
 */