package org.mastermind;

import org.mastermind.solver.BestGuess;
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
        long[] bestGuess = BestGuess.findBestGuess(state.allInd, state.allInd, BenchmarkState.C, BenchmarkState.D,
                                                   false);
        blackhole.consume(bestGuess);
    }

    // Parallel Version
    @Benchmark
    public void benchmarkParallelVersion(BenchmarkState state, Blackhole blackhole) {
        long[] bestGuess = BestGuess.findBestGuess(state.allInd, state.allInd, BenchmarkState.C, BenchmarkState.D,
                                                   true);
        blackhole.consume(bestGuess);
    }

    @State(Scope.Thread)
    public static class BenchmarkState {
        static final int C = 6, D = 4;
        private final int[] allInd;

        public BenchmarkState() {
            allInd = new int[(int) Math.pow(C, D)];
            for (int i = 0; i < allInd.length; i++) allInd[i] = i;
        }
    }
}

/* Average Performance:
Benchmark                                    Mode  Cnt   Score   Error  Units
BestGuessBenchmark.benchmarkOrdinaryVersion  avgt    6  35.945 ± 4.358  ms/op
BestGuessBenchmark.benchmarkParallelVersion  avgt    6  21.431 ± 3.777  ms/op
 */