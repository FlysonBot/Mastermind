### Project Overview

Mastermind solver using Java algorithms (performance) + Python UI (terminal).
Goal: Efficiently solve c=9, d=9 cases.
Status: Java algorithm complete. Python UI in progress.

### Code Organization

- **Java algorithm**: `./src/main/java/org/mastermind/`
- **Java tests**: `./src/tests/java/org/mastermind/` (JUnit 5)
- **Java benchmarks**: `./src/benchmarks/java/org/mastermind/` (JMH)
- **Python UI**: `./src/main/python/mastermind/`
  - `jvm.py` — starts the JVM and imports Java classes
  - `main.py` — entry point and game loop
  - `ui.py` — terminal rendering and input parsing
- **Build**: `make build-java` → `target/mastermind-solver.jar`
- Everything else is legacy—ignore unless explicitly instructed.

### Algorithm Flow

1. `Feedback.getFeedback()` — calculates feedback for guess vs. secret
2. `ExpectedSize.calcExpectedRank()` — estimates solution space size after a guess
3. `BestGuess.findBestGuess()` — finds optimal guess by evaluating all candidates
4. `SolutionSpace` — tracks remaining valid solutions
5. `GuessStrategy.select()` — chooses which guesses and secrets arrays to pass into `BestGuess`
6. `MastermindSession` — manages a full game: history, solution space, strategy-based suggestions, undo

### Current Focus

- Python UI (terminal). Java side is complete.

### Preference

- Stick to primitive type unless there is a reason not to.
- Unless necessary, do not write extra class and objects. Be simple.
- Do not run any tests or benchmark for me unless specifically instructed.
- DO NOT TOUCH the average performance in benchmarks. Don't delete, don't modify, don't change, don't update.