### Project Overview

Mastermind solver using Java algorithms (performance) + Python UI (terminal).
Goal: Efficiently solve c=9, d=9 cases.
Status: MVP shipped to PyPI. Now improving the Python UI.

### Code Organization

- **Java algorithm**: `./src/main/java/org/mastermind/`
- **Java tests**: `./src/tests/java/org/mastermind/` (JUnit 5)
- **Java benchmarks**: `./src/benchmarks/java/org/mastermind/` (JMH)
- **Python program**: `./src/main/python/mastermind/` (entry point: `main.py`)
- **Python tests**: `./src/tests/python/mastermind/` (pytest)
- **Build**: `make build-java` → `target/mastermind-solver.jar`

### Algorithm Flow

1. `Feedback.getFeedback()` — calculates feedback for guess vs. secret
2. `ExpectedSize.calcExpectedRank()` — estimates solution space size after a guess
3. `BestGuess.findBestGuess()` — finds optimal guess by evaluating all candidates
4. `SolutionSpace` — tracks remaining valid solutions
5. `GuessStrategy.select()` — chooses which guesses and secrets arrays to pass into `BestGuess`
6. `MastermindSession` — manages a full game: history, solution space, strategy-based suggestions, undo

### UI Flow

Entry: `main.py` → `java_setup.ensure_ready()` → `welcome.welcome()` (main menu loop)

#### Gamemodes (`gamemode/`):

- **Play** (`human.py`) — Player guesses a code. Secret is set by computer or another person; player enters guesses and
  receives black/white feedback.
- **Watch** (`computer.py`) — Algorithm solves the code. Secret is set by computer or the player; algorithm suggests and
  plays each guess automatically.
- **Assist** (`assisted.py`) — Player is playing a real-life game; algorithm suggests the best guess each turn. Player
  enters their actual guess and the feedback they received; algorithm tracks the solution space and narrows it down.

#### Other modules:

- `welcome.py` — Banner and main menu loop
- `jvm.py` — JPype bridge to the Java JAR
- `java_setup.py` — Ensures JRE and JAR are present before starting

### Current Focus

- Improve Python UI using rich.

### Preference

- Stick to primitive type unless there is a reason not to.
- Unless necessary, do not write extra class and objects. Be simple.
- Do not run any tests or benchmark for me unless specifically instructed.
- DO NOT TOUCH the average performance in benchmarks. Don't delete, don't modify, don't change, don't update.