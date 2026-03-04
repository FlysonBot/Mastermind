package org.mastermind.codes;

import org.mastermind.solver.Feedback;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.BitSet;
import java.util.concurrent.TimeUnit;

/**
 * Benchmarks getValidSample for c=9, d=9 at fill rates spanning both the
 * enumeration path (validCount <= 5M) and the rejection path (validCount > 5M).
 * Goal: confirm that sampling time stays small regardless of fill rate.
 */
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 2, time = 1)
@Measurement(iterations = 2, time = 1)
@Fork(1)
public class SampledCodeBenchmark {

    // ── Benchmarks ────────────────────────────────────────────────────────────

    private static BitSet buildBitSet(double fillRate) {
        int    total = (int) Math.pow(9, 9);
        int    count = (int) (fillRate * total);
        BitSet bs    = new BitSet(total);
        if (count >= total) {
            bs.set(0, total);
        } else {
            double step = (double) total / count;
            for (int i = 0; i < count; i++) bs.set((int) (i * step));
        }
        return bs;
    }

    @Benchmark
    public void sample_enum_1pct(Fill1pct state, Blackhole bh) {
        bh.consume(SampledCode.getValidSample(state.remaining, state.validCount, 9, 9, state.sampleSize));
    }

    @Benchmark
    public void sample_enum_05pct(Fill05pct state, Blackhole bh) {
        bh.consume(SampledCode.getValidSample(state.remaining, state.validCount, 9, 9, state.sampleSize));
    }

    @Benchmark
    public void sample_reject_2pct(Fill2pct state, Blackhole bh) {
        bh.consume(SampledCode.getValidSample(state.remaining, state.validCount, 9, 9, state.sampleSize));
    }

    @Benchmark
    public void sample_reject_5pct(Fill5pct state, Blackhole bh) {
        bh.consume(SampledCode.getValidSample(state.remaining, state.validCount, 9, 9, state.sampleSize));
    }

    @Benchmark
    public void sample_reject_10pct(Fill10pct state, Blackhole bh) {
        bh.consume(SampledCode.getValidSample(state.remaining, state.validCount, 9, 9, state.sampleSize));
    }

    @Benchmark
    public void sample_reject_50pct(Fill50pct state, Blackhole bh) {
        bh.consume(SampledCode.getValidSample(state.remaining, state.validCount, 9, 9, state.sampleSize));
    }

    // ── States ────────────────────────────────────────────────────────────────

    @Benchmark
    public void sample_reject_100pct(Fill100pct state, Blackhole bh) {
        bh.consume(SampledCode.getValidSample(state.remaining, state.validCount, 9, 9, state.sampleSize));
    }

    @State(Scope.Thread)
    public static class BaseState {
        final int sampleSize = SampledCode.calcSampleSizeForSecrets(Feedback.calcFeedbackSize(9));
    }

    // Enumeration path (validCount <= MAX_ENUM = 5M)
    @State(Scope.Thread)
    public static class Fill05pct extends BaseState {
        // 0.5%: validCount ≈ 1.9M — enum
        final BitSet remaining  = buildBitSet(0.005);
        final int    validCount = remaining.cardinality();
    }

    @State(Scope.Thread)
    public static class Fill1pct extends BaseState {
        // 1%: validCount ≈ 3.9M — enum
        final BitSet remaining  = buildBitSet(0.010);
        final int    validCount = remaining.cardinality();
    }

    // Rejection path (validCount > MAX_ENUM = 5M)
    @State(Scope.Thread)
    public static class Fill2pct extends BaseState {
        // 2%: validCount ≈ 7.7M — reject
        final BitSet remaining  = buildBitSet(0.020);
        final int    validCount = remaining.cardinality();
    }

    @State(Scope.Thread)
    public static class Fill5pct extends BaseState {
        // 5%: validCount ≈ 19M — reject
        final BitSet remaining  = buildBitSet(0.050);
        final int    validCount = remaining.cardinality();
    }

    @State(Scope.Thread)
    public static class Fill10pct extends BaseState {
        // 10%: validCount ≈ 39M — reject
        final BitSet remaining  = buildBitSet(0.100);
        final int    validCount = remaining.cardinality();
    }

    @State(Scope.Thread)
    public static class Fill50pct extends BaseState {
        // 50%: validCount ≈ 194M — reject
        final BitSet remaining  = buildBitSet(0.500);
        final int    validCount = remaining.cardinality();
    }

    // ── Helper ────────────────────────────────────────────────────────────────

    @State(Scope.Thread)
    public static class Fill100pct extends BaseState {
        // 100%: validCount = 387M — reject
        final BitSet remaining  = buildBitSet(1.000);
        final int    validCount = remaining.cardinality();
    }
}

/* Average Performance:
Benchmark                                  Mode  Cnt   Score   Error  Units
SampledCodeBenchmark.sample_enum_05pct     avgt    2  12.344          ms/op
SampledCodeBenchmark.sample_enum_1pct      avgt    2  19.482          ms/op
SampledCodeBenchmark.sample_reject_100pct  avgt    2   0.400          ms/op
SampledCodeBenchmark.sample_reject_10pct   avgt    2   3.953          ms/op
SampledCodeBenchmark.sample_reject_2pct    avgt    2  19.607          ms/op
SampledCodeBenchmark.sample_reject_50pct   avgt    2   0.833          ms/op
SampledCodeBenchmark.sample_reject_5pct    avgt    2   7.851          ms/op
 */
