package org.mastermind;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 5, time = 1)
@Measurement(iterations = 20, time = 2)
@Fork(1)
public class FeedbackBenchmark {  // ← MAIN CLASS

    // 1. STATE CLASS (nested static class)
    @State(Scope.Thread)
    public static class BenchmarkState {
        public int getFeedbackQuick(int guess, int secret) {
            return Feedback.getFeedback(guess, secret, 4);
        }
    }

    // 2. BENCHMARK METHOD (top-level in main class)
    @Benchmark
    public void benchmarkTest(BenchmarkState state, Blackhole blackhole) {
        int feedback = state.getFeedbackQuick(1234, 4263);
        blackhole.consume(feedback);
    }
}