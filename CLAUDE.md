### Project Overview

Mastermind solver using Java algorithms (performance) + Python UI (terminal).
Goal: Efficiently solve c=9, d=9 cases.
Status: Rewriting codebase; currently focused on Java algorithm only.

### Code Organization

- **Active**: `./src/main/java/org/mastermind/` (algorithm)
- **Tests**: `./src/tests/java/org/mastermind/` (JUnit 5)
- **Benchmarks**: `./src/benchmarks/java/org/mastermind/` (JMH)
- Everything else is legacy—ignore unless explicitly instructed.

### Algorithm Flow

1. `Feedback.getFeedback()` — calculates feedback for guess vs. secret
2. `ExpectedSize.calcExpectedRank()` — estimates solution space size after a guess
3. `BestGuess.findBestGuess()` — finds optimal guess by evaluating all candidates
4. `SolutionSpace` — tracks remaining valid solutions
5. `GuessStrategy.select()` — chooses which guesses and secrets arrays to pass into `BestGuess`
6. `MastermindSession` — manages a full game: history, solution space, strategy-based suggestions, undo

### Next Move / Current Move

- IMPORTANT: Currently trying to do large scale refactor class-by-class step-by-step to deprecate int[] array
  for passing combinations around, and instead uses BitSet

### Preference

- Stick to primitive type unless there is a reason not to.
- Unless necessary, do not write extra class and objects. Be simple.
- Do not run any tests or benchmark for me unless specifically instructed.