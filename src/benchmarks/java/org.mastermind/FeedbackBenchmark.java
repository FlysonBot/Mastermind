package org.mastermind;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@Warmup(iterations = 4, time = 1)
@Measurement(iterations = 4, time = 1)
@Fork(1)
public class FeedbackBenchmark {

    // 1. STATE CLASS (nested static class)
    @State(Scope.Thread)
    public static class BenchmarkState {
        public int[] secrets = AllValidCode.generateAllCodes(6, 4);
        public int[] freq = new int[10];
        public int getFeedbackQuick(int guess, int secret) {
            return Feedback.getFeedback(guess, secret, 4, freq);
        }
    }

    // 2. BENCHMARK METHOD
    @OutputTimeUnit(TimeUnit.NANOSECONDS)
    @Benchmark
    public void fixInputBenchmark(BenchmarkState state, Blackhole blackhole) {
        int feedback = state.getFeedbackQuick(1234, 4263);
        blackhole.consume(feedback);
    }

    @OutputTimeUnit(TimeUnit.MICROSECONDS)
    @Benchmark
    public void oneVariedInputBenchmark(BenchmarkState state, Blackhole blackhole) {
        for (int secret: state.secrets) {
            int feedback = state.getFeedbackQuick(1234, secret);
            blackhole.consume(feedback);
        }
    }

    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    @Benchmark
    public void doubleVariedInputBenchmark(BenchmarkState state, Blackhole blackhole) {
        for (int guess: state.secrets) {
            for (int secret : state.secrets) {
                int feedback = state.getFeedbackQuick(guess, secret);
                blackhole.consume(feedback);
            }
        }
    }
}

/* Benchmark average:
Benchmark                                     Mode  Cnt   Score   Error  Units
FeedbackBenchmark.doubleVariedInputBenchmark  avgt    4  31.701 ± 0.710  ms/op
FeedbackBenchmark.fixInputBenchmark           avgt    4  17.730 ± 0.594  ns/op
FeedbackBenchmark.oneVariedInputBenchmark     avgt    4  22.019 ± 0.465  us/op
 */