# Contribution Guidelines

Please note that this project is released with a [Contributor Code](https://github.com/FlysonBot/Mastermind/blob/main/CODE_OF_CONDUCT.md) of Conduct. By participating in this project you agree to abide by its terms.

## Guidelines on Programming

### Coding Style and Quality

- Use [`Ruff`](https://github.com/astral-sh/ruff) or formatting Python code, follow PEP8 convention.
- Use type hints for all Python functions including return type. Unless it is in a test.
- Add empty line after `if`/`else`/`elif`/`try`/`except` blocks to improve readability.
- Write code that are self-documenting (descriptive function and variable names).
- Include detailed docstring for critical methods.
- Do comprehensive testing. 

### Use of AI for Code

Use of AI is encouraged to improve the quality of the code and to write comprehensive tests. However, make sure you reviewed the code and understand it before using it.

The project is currently using Claude Code to assist with coding. A CLAUDE.md file is included in the project root.

## PR and Commit Guidelines

- All changes should be proposed through the use of [Pull Request (PR)](https://github.com/FlysonBot/Mastermind/pulls)
- All commit should follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0) format.
- All PR should include clear description of what is being done.
- Ensure you do not write too big of a PR as that make the reviewing more difficult.
