package org.mastermind;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 3, time = 1)
@Fork(5)
public class BestGuessBenchmark {

    // 1. STATE CLASS (nested static class)
    @State(Scope.Thread)
    public static class BenchmarkState {
        private final int[] allCodes = AllValidCode.generateAllCodes(6, 4);
    }

    // 2. BENCHMARK METHOD
    @Benchmark
    public void benchmarkTest(BenchmarkState state, Blackhole blackhole) {
        int bestGuess = BestGuess.findBestGuess(state.allCodes, state.allCodes, 4);
        blackhole.consume(bestGuess);
    }
}

/* Average Performance:
Benchmark                         Mode  Cnt   Score   Error  Units
BestGuessBenchmark.benchmarkTest  avgt   15  34.629 ± 0.476  ms/op
 */