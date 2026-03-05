package org.mastermind.compute;

import org.mastermind.codes.ConvertCode;
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
        state.space.filterSolution(state.guessInd, state.feedback);
        state.space.reset();
    }

    /**
     * Benchmark filterSolution on a large (c=9,d=5) space — exercises the parallel path.
     */
    @Benchmark
    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    public void filterParallelFull(LargeState state) {
        state.space.filterSolution(state.guessInd, state.feedback);
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
        int           guessInd;
        int           feedback;
        int[]         freq = new int[C];

        static int ind(int code) { return ConvertCode.toIndex(C, D, code); }

        @Setup(Level.Trial)
        public void setup() {
            space = new SolutionSpace(C, D);
            guessInd = ind(1122);
            feedback = Feedback.getFeedback(guessInd, ind(3456), C, D, freq);
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
        int           guessInd;
        int           feedback;
        int[]         freq = new int[C];

        static int ind(int code) { return ConvertCode.toIndex(C, D, code); }

        @Setup(Level.Trial)
        public void setup() {
            space = new SolutionSpace(C, D);
            guessInd = ind(11223);
            feedback = Feedback.getFeedback(guessInd, ind(34567), C, D, freq);
        }

        @Setup(Level.Invocation)
        public void reset() {
            space.reset();
        }
    }
}

/* Average Performance:
Benchmark                                  Mode  Cnt   Score   Error  Units
SolutionSpaceBenchmark.filterParallelFull  avgt    4   0.608 ± 0.195  ms/op
SolutionSpaceBenchmark.filterSerialFull    avgt    4  38.088 ± 2.371  us/op
SolutionSpaceBenchmark.getSecretsFull      avgt    4   5.723 ± 0.188  us/op
SolutionSpaceBenchmark.getSize             avgt    4  18.442 ± 0.872  ns/op
 */