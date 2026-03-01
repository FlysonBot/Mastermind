package org.mastermind;

import org.mastermind.codes.SampledCode;
import org.mastermind.solver.Feedback;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 3, time = 1)
@Fork(5)
public class SampledCodeBenchmark {

    @Benchmark
    public void benchmarkGetSample(BenchmarkState state, Blackhole blackhole) {
        int[] sample = SampledCode.getSample(9, 9, state.sampleSize);
        blackhole.consume(sample);
    }

    @State(Scope.Thread)
    public static class BenchmarkState {
        // feedbackSize for d=9: (9+1)*(9+2)/2 = 55
        final int sampleSize = SampledCode.calcSampleSizeForSecrets(Feedback.calcFeedbackSize(9));
    }
}

/* Average Performance:
Benchmark                                Mode  Cnt  Score   Error  Units
SampledCodeBenchmark.benchmarkGetSample  avgt   15  9.964 ± 0.152  ms/op
 */