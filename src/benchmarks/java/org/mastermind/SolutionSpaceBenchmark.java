package org.mastermind;

import org.mastermind.solver.Feedback;
import org.mastermind.solver.SolutionSpace;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@Warmup(iterations = 4, time = 1)
@Measurement(iterations = 4, time = 1)
@Fork(1)
public class SolutionSpaceBenchmark {

    /**
     * Benchmark filterSolution on a small (c=6,d=4) space — exercises the serial path.
     * Reset is done per-invocation since filterSolution mutates state.
     */
    @Benchmark
    @OutputTimeUnit(TimeUnit.MICROSECONDS)
    public void filterSerialFull(SmallState state) {
        state.space.filterSolution(state.guess, state.feedback);
        state.space.reset();
    }

    /**
     * Benchmark filterSolution on a large (c=9,d=5) space — exercises the parallel path.
     */
    @Benchmark
    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    public void filterParallelFull(LargeState state) {
        state.space.filterSolution(state.guess, state.feedback);
        state.space.reset();
    }

    /**
     * Benchmark getSecrets on a full small (c=6,d=4) space.
     */
    @Benchmark
    @OutputTimeUnit(TimeUnit.MICROSECONDS)
    public void getSecretsFull(SmallState state, Blackhole blackhole) {
        blackhole.consume(state.space.getSecrets());
    }

    /**
     * Benchmark getSize — O(1) counter read.
     */
    @Benchmark
    @OutputTimeUnit(TimeUnit.NANOSECONDS)
    public void getSize(SmallState state, Blackhole blackhole) {
        blackhole.consume(state.space.getSize());
    }

    @State(Scope.Thread)
    public static class SmallState {
        static final int C = 6, D = 4;
        SolutionSpace space;
        int           guess;
        int           feedback;
        int[]         freq = new int[10];

        @Setup(Level.Trial)
        public void setup() {
            space = new SolutionSpace(C, D);
            guess = 1122;
            feedback = Feedback.getFeedback(guess, 3456, C, D, freq);
        }

        @Setup(Level.Invocation)
        public void reset() {
            space.reset();
        }
    }

    @State(Scope.Thread)
    public static class LargeState {
        static final int C = 9, D = 5;
        SolutionSpace space;
        int           guess;
        int           feedback;
        int[]         freq = new int[10];

        @Setup(Level.Trial)
        public void setup() {
            space = new SolutionSpace(C, D);
            guess = 11223;
            feedback = Feedback.getFeedback(guess, 34567, C, D, freq);
        }

        @Setup(Level.Invocation)
        public void reset() {
            space.reset();
        }
    }
}

/* Average Performance:
Benchmark                                  Mode  Cnt   Score   Error  Units
SolutionSpaceBenchmark.filterParallelFull  avgt    4   0.632 ± 0.672  ms/op
SolutionSpaceBenchmark.filterSerialFull    avgt    4  30.677 ± 2.271  us/op
SolutionSpaceBenchmark.getSecretsFull      avgt    4   6.024 ± 0.218  us/op
SolutionSpaceBenchmark.getSize             avgt    4  17.925 ± 0.885  ns/op
 */