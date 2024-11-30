# Contribution Guidelines

Please note that this project is released with a [Contributor Code](https://github.com/FlysonBot/Mastermind/blob/main/CODE_OF_CONDUCT.md) of Conduct. By participating in this project you agree to abide by its terms.

## Guidelines on Programming

### Coding Style and Quality

- Use [`Black`](https://github.com/psf/black) and [`isort`](https://pycqa.github.io/isort/) for formatting (or [`Ruff`](https://github.com/astral-sh/ruff) as their equivalence), follow PEP8 convention.
- Use type hints for all functions including return type. Unless it is in a test.
- Add empty line after `if`/`else`/`elif`/`try`/`except` blocks to improve readability.
- Write code that are self-documenting (descriptive function and variable names).
- Include detailed docstring for critical methods.
- Create a test file for each module, a test class for each class, and a test method for each method.

### Use of AI for Code

Use of AI is encouraged to improve the quality of the code and to write comprehensive tests. However, make sure you reviewed the code and understand it before using it.

## PR and Commit Guidelines

- All changes should be proposed through the use of [Pull Request (PR)](https://github.com/FlysonBot/Mastermind/pulls)
- All commit should follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0) format.
- All PR should include clear description of what is being done.
- Ensure you do not write too big of a PR as that make the reviewing more difficult.
