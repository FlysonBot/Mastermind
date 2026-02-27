package org.mastermind;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 3, time = 1)
@Fork(2)
public class BestGuessBenchmark {

    // Ordinary (Sequential) Version
    @Benchmark
    public void benchmarkOrdinaryVersion(BenchmarkState state, Blackhole blackhole) {
        long[] bestGuess = BestGuess.findBestGuess(state.allCodes, state.allCodes, 4, false);
        blackhole.consume(bestGuess);
    }

    // Parallel Version
    @Benchmark
    public void benchmarkParallelVersion(BenchmarkState state, Blackhole blackhole) {
        long[] bestGuess = BestGuess.findBestGuess(state.allCodes, state.allCodes, 4, true);
        blackhole.consume(bestGuess);
    }

    @State(Scope.Thread)
    public static class BenchmarkState {
        private final int[] allCodes = AllValidCode.generateAllCodes(6, 4);

        // TEARDOWN - Shutdown the thread pool after benchmarking
        @TearDown(Level.Trial)
        public void tearDown() {
            BestGuess.shutdown();
        }
    }
}

/* Average Performance:
Benchmark                                    Mode  Cnt   Score   Error  Units
BestGuessBenchmark.benchmarkOrdinaryVersion  avgt    6  34.278 ± 0.994  ms/op
BestGuessBenchmark.benchmarkParallelVersion  avgt    6  12.409 ± 4.445  ms/op
 */