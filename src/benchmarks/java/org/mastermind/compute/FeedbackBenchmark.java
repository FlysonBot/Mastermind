package org.mastermind.compute;

import org.mastermind.codes.ConvertCode;
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

    @OutputTimeUnit(TimeUnit.MICROSECONDS)
    @Benchmark
    @Fork(4)
    public void oneVariedInputIncrementalBenchmark(BenchmarkState state, Blackhole blackhole) {
        int   guessInd    = BenchmarkState.ind(1234);
        int   c           = BenchmarkState.C, d = BenchmarkState.D;
        int[] guessDigits = state.guessDigits;
        int   tmp         = guessInd;
        for (int p = 0; p < d; p++) {
            guessDigits[p] = tmp % c;
            tmp /= c;
        }

        // Bootstrap at secretInd=0
        int[] colorFreqCounter = state.colorFreqCounter;
        java.util.Arrays.fill(colorFreqCounter, 0);
        int   feedback0    = Feedback.getFeedback(guessInd, 0, c, d, state.freq);
        int   black        = 0;
        int[] secretDigits = state.secretDigits;
        for (int p = 0; p < d; p++) { secretDigits[p] = 0; }
        for (int p = 0; p < d; p++) {
            int gs = guessDigits[p];
            if (gs == 0) black++;
            else {
                colorFreqCounter[gs]++;
                colorFreqCounter[0]--;
            }
        }
        int colorFreqTotal = 0;
        for (int i = 0; i < c; i++) {
            int f = colorFreqCounter[i];
            colorFreqTotal += f > 0 ? f : -f;
        }
        blackhole.consume(feedback0);

        int[] result = state.result;
        for (int secretInd = 1; secretInd < state.total; secretInd++) {
            FeedbackIncremental.getFeedbackIncremental(guessDigits, secretDigits, black, colorFreqCounter,
                                                       colorFreqTotal, c, d,
                                                       result);
            black = result[1];
            colorFreqTotal = result[2];
            blackhole.consume(result[0]);
        }
    }

    @State(Scope.Thread)
    public static class BenchmarkState {
        static final int C = 6, D = 4;
        public int   total            = (int) Math.pow(C, D); // 1296
        public int[] freq             = new int[C];
        // Incremental benchmark state (reused across iterations to avoid allocation in hot loop)
        public int[] guessDigits      = new int[D];
        public int[] secretDigits     = new int[D];
        public int[] colorFreqCounter = new int[C];
        public int[] result           = new int[3];

        public static int ind(int code) { return ConvertCode.toIndex(C, D, code); }

        public int getFeedbackQuick(int guessIdx, int secretIdx) {
            return Feedback.getFeedback(guessIdx, secretIdx, C, D, freq);
        }
    }
}

/* Average Performance:
Benchmark                                     Mode  Cnt   Score   Error  Units
FeedbackBenchmark.doubleVariedInputBenchmark          avgt    4  30.815 ± 3.831  ms/op
FeedbackBenchmark.fixInputBenchmark                   avgt    4  18.644 ± 0.701  ns/op
FeedbackBenchmark.oneVariedInputBenchmark             avgt    4  26.329 ± 6.294  us/op
FeedbackBenchmark.oneVariedInputIncrementalBenchmark  avgt   16  4.679 ± 0.150  us/op
 */