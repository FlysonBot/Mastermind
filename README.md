<p align="center">
<img src="Mastermind Logo.svg" width="350" title="Mastermind Logo" alt="Mastermind Logo">
</p>

| **Version:** | [![GitHub tag](https://img.shields.io/github/tag/FlysonBot/Mastermind?include_prereleases=&sort=semver&color=blue)](https://github.com/FlysonBot/Mastermind/tags) [![GitHub Release](https://img.shields.io/github/v/release/FlysonBot/Mastermind?include_prereleases)](https://github.com/FlysonBot/Mastermind/releases) [![Python Version](https://img.shields.io/pypi/pyversions/mastermind-ai)](https://www.python.org/downloads/) [![PyPI - Version](https://img.shields.io/pypi/v/mastermind-ai)](https://pypi.org/project/mastermind-ai/) |
| --- | :-: |
| **Meta:** | [![GitHub License](https://img.shields.io/github/license/FlysonBot/Mastermind)](https://github.com/FlysonBot/Mastermind/blob/main/LICENSE) ![PyPI Status](https://img.shields.io/pypi/status/mastermind-ai) ![Repo Size](https://img.shields.io/github/repo-size/FlysonBot/Mastermind) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/FlysonBot/Mastermind/main.svg)](https://results.pre-commit.ci/latest/github/FlysonBot/Mastermind/main) |

**Links:**

- [Documentation](https://flysonbot.github.io/Mastermind/)
- [Source Code](https://github.com/FlysonBot/Mastermind)
- [Releases](https://github.com/FlysonBot/Mastermind/releases)
- [Bug Reports](https://github.com/FlysonBot/Mastermind/issues)
- [Play Online on Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/examples/mastermind_in_colab.ipynb)

# Mastermind

> A terminal Mastermind game with 4 modes and a built-in magic solver. Install with pip and play in seconds — no
> configuration needed.

## What is Mastermind?

Mastermind is a classic code-breaking game: one player hides a secret code, the other tries to crack it. After each
guess, you get feedback on how close you are — and you have to use that to narrow it down before you run out of
attempts. Simple to learn, surprisingly deep to master.

## Features

- **Play** — Guess the secret code yourself
- **Watch** — Let the AI solve it optimally
- **Assist** — Get AI suggestions while playing a real game
- **Rules** — Learn how to play

## Getting Started

### Prerequisites

Just install Python 3.12+ and pip — the Java runtime is bundled for Linux, Windows, and macOS.

> For Android, install [Termux](https://termux.dev/) and run `pkg install openjdk-21` first.

<details>
<summary><i>Technical Details for Developers</i></summary>

- **JPype**: bridges Python and Java at runtime, allowing the Python UI to call into the high-performance Java solver directly without a subprocess.

</details>

### Installation

1. Install [Python 3.12+](https://www.python.org/downloads/) if you haven't already.

2. Install the latest release:

    ```bash
    pip install mastermind-ai
    ```

3. Run the program:

    ```bash
    mastermind
    ```

> [!TIP]
> If the above does not work, see the [Troubleshooting Guide](.github/TROUBLESHOOTING.md).

You can also try it in your browser with [Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/examples/mastermind_in_colab.ipynb).

## Contributing

Contributions are welcome! See the [Contributing Guidelines](.github/CONTRIBUTING.md).

## License

Licensed under [MIT License](https://github.com/FlysonBot/Mastermind/blob/main/LICENSE) by [@FlysonBot](https://github.com/FlysonBot).

## Questions?

Feel free to leave questions in the [Discussions](https://github.com/FlysonBot/Mastermind/discussions) or open an [Issue](https://github.com/FlysonBot/Mastermind/issues).
