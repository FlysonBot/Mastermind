package org.mastermind;

import org.mastermind.codes.ConvertCode;
import org.mastermind.solver.Feedback;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@Warmup(iterations = 4, time = 1)
@Measurement(iterations = 4, time = 1)
@Fork(1)
public class FeedbackBenchmark {

    @OutputTimeUnit(TimeUnit.NANOSECONDS)
    @Benchmark
    public void fixInputBenchmark(BenchmarkState state, Blackhole blackhole) {
        int feedback = state.getFeedbackQuick(BenchmarkState.ind(1234), BenchmarkState.ind(4263));
        blackhole.consume(feedback);
    }

    @OutputTimeUnit(TimeUnit.MICROSECONDS)
    @Benchmark
    public void oneVariedInputBenchmark(BenchmarkState state, Blackhole blackhole) {
        for (int secretIdx = 0; secretIdx < state.total; secretIdx++) {
            int feedback = state.getFeedbackQuick(BenchmarkState.ind(1234), secretIdx);
            blackhole.consume(feedback);
        }
    }

    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    @Benchmark
    public void doubleVariedInputBenchmark(BenchmarkState state, Blackhole blackhole) {
        for (int guessIdx = 0; guessIdx < state.total; guessIdx++) {
            for (int secretIdx = 0; secretIdx < state.total; secretIdx++) {
                int feedback = state.getFeedbackQuick(guessIdx, secretIdx);
                blackhole.consume(feedback);
            }
        }
    }

    @State(Scope.Thread)
    public static class BenchmarkState {
        static final int C = 6, D = 4;
        public int   total = (int) Math.pow(C, D); // 1296
        public int[] freq  = new int[C];

        public static int ind(int code) { return ConvertCode.toIndex(C, D, code); }

        public int getFeedbackQuick(int guessIdx, int secretIdx) {
            return Feedback.getFeedback(guessIdx, secretIdx, C, D, freq);
        }
    }
}

/* Benchmark average:
Benchmark                                     Mode  Cnt   Score   Error  Units
FeedbackBenchmark.doubleVariedInputBenchmark  avgt    4  29.915 ± 3.150  ms/op
FeedbackBenchmark.fixInputBenchmark           avgt    4  18.171 ± 1.001  ns/op
FeedbackBenchmark.oneVariedInputBenchmark     avgt    4  25.012 ± 0.728  us/op
 */