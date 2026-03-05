### Project Overview

Mastermind solver using Java algorithms (performance) + Python UI (terminal).
Goal: Efficiently solve c=9, d=9 cases.
Status: Java algorithm complete and performing well (~2s for a full 9x9 solve). Currently in cleanup phase (comments,
tests, chores). Python UI not yet started.

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

### Current Focus

- Java side mostly done; touching up code quality, expanding test coverage, misc chores.
- Next major phase: Python UI.

### Preference

- Stick to primitive type unless there is a reason not to.
- Unless necessary, do not write extra class and objects. Be simple.
- Do not run any tests or benchmark for me unless specifically instructed.
- DO NOT TOUCH the average performance in benchmarks. Don't delete, don't modify, don't change, don't update.