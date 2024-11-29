<p align="center">
<img src="https://raw.githubusercontent.com/FlysonBot/Mastermind/main/docs/source/_static/Mastermind Logo.svg" width="350">
</p>

| | |
| --- | --- |
| **Testing:** | [![Testing Status](https://img.shields.io/github/actions/workflow/status/FlysonBot/Mastermind/coveralls.yaml?label=test)](https://github.com/FlysonBot/Mastermind/actions/workflows/coveralls.yaml) [![Test Coverage](https://coveralls.io/repos/github/FlysonBot/Mastermind/badge.svg?branch=main)](https://coveralls.io/github/FlysonBot/Mastermind?branch=main)  [![CodeFactor](https://www.codefactor.io/repository/github/flysonbot/mastermind/badge/main)](https://www.codefactor.io/repository/github/flysonbot/mastermind/overview/main) [![Docs Deploy Status](https://img.shields.io/github/actions/workflow/status/FlysonBot/Mastermind/deploy_sphinx.yaml?label=docs)](https://flysonbot.github.io/Mastermind/) |
| **Version:** | [![GitHub tag](https://img.shields.io/github/tag/FlysonBot/Mastermind?include_prereleases=&sort=semver&color=blue)](https://github.com/FlysonBot/Mastermind/tags) [![GitHub Release](https://img.shields.io/github/v/release/FlysonBot/Mastermind)](https://github.com/FlysonBot/Mastermind/releases) [![Python Version](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/downloads/) |
| **Repo:** | [![GitHub Downloads](https://img.shields.io/github/downloads/FlysonBot/Mastermind/total)](https://github.com/FlysonBot/Mastermind/releases) [![Opened Issue Count](https://img.shields.io/github/issues/FlysonBot/Mastermind)](https://github.com/FlysonBot/Mastermind/issues) [![Closed Issue Count](https://img.shields.io/github/issues-closed/FlysonBot/Mastermind)](https://github.com/FlysonBot/Mastermind/issues?q=is%3Aissue+is%3Aclosed) [![Closed PR Count](https://img.shields.io/github/issues-pr-closed/FlysonBot/Mastermind)](https://github.com/FlysonBot/Mastermind/pulls?q=is%3Apr+is%3Aclosed) ![Repo Size](https://img.shields.io/github/repo-size/FlysonBot/Mastermind) |
| **Meta:** | [![GitHub License](https://img.shields.io/github/license/FlysonBot/Mastermind)](https://github.com/FlysonBot/Mastermind/blob/main/LICENSE) |

> [!NOTE]  
> This repo is currently still under development. Currently there is a beta version that have the basic simulation feature finished. If you encountered any issue, please open up an issue and let me know! I'll try to fix them as soon as possible.

# Mastermind

> This is a python implementation of the classic puzzle game Mastermind. It simulates the game and allow you to play with either another human being (sits next to you) or the computer, with a AI Solver build-in (still under development). You can install this game with pip or try it out in your browser with [Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/mastermind_in_colab.ipynb).

## What is Mastermind?

Mastermind is a code-breaking game for two players. The first player (the code-setter) creates a secret code, which the second player (the code-cracker) tries to guess. The code-cracker has a limited number of attempts to guess the code correctly. After each guess, the code-setter provides feedback to the code-cracker, indicating how many dots have the right color and are in the right place, and how many are the right color but in the wrong place. The code-cracker uses this feedback to refine their guesses until they correctly guess the code or run out of attempts.

## Getting Started

### Prerequisites

To run this project, you must have the following installed (installation guide below):

- Git (needed to clone this repository)
- Python 3.10 (or higher)
- pip (comes with Python, needed to install the project as a library)

Or alternatively you can run this program in your browser with [Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/mastermind_in_colab.ipynb)

### Installation Guide

1. Install [Git](https://git-scm.com/downloads) if you haven't already.

2. Install [Python 3.10+](https://www.python.org/downloads/) if you haven't already.

3. Install this repository as a python library using the following command in your terminal:

    ```bash
    pip install git+https://github.com/FlysonBot/Mastermind.git
    ```

4. Run the program with the following command:

    ```bash
    mastermind
    ```

5. Enjoy!

> [!TIP]
> If the above doesn't work, try the troubleshooting guide below.

### Troubleshooting

If you encounter any issues during installation, please check the following:

1. Do you have trouble finding your terminal?

    - For windows users, press `Ctrl + R` and type `cmd` and press enter.
    - For mac users, press `Cmd + Space` and type `terminal` and press enter.
    - For linux users, press `Ctrl + Alt + T`.

2. Do you have `git` installed properly? Check with the following command:

    ```bash
    git --version
    ```

    If you get an error, you need to install git.

3. Do you have the correct version of `python` installed? Check with the following command:

    ```bash
    python --version
    ```

    If you get an error, you need to install python.
    If your python version is lower than 3.10, you need to upgrade your python version.

4. Do you have `pip` installed properly? Check with the following command:

    ```bash
    pip --version
    ```

    If you get an error, you need to install `pip`.

5. Did you encountered an error associated with installing the dependencies of this project? Try installing the dependencies manually using the following command:

    ```bash
    pip install pandas
    ```

    If you get an error, the dependencies doesn't work on your machine. You'll have to find your own way to install the dependencies.

6. If you're still having trouble, please open an issue on the [GitHub repository](https://github.com/FlysonBot/Mastermind/issues) and we'll try to help you out. Or alternatively you can run the program in your [browser](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/mastermind_in_colab.ipynb)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

All contributors must adhere to the [Contributor Covenant Code of Conduct](https://github.com/FlysonBot/Mastermind/blob/main/CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive environment for all contributors.

To contribute to the code directly, you must also follow the [Contributing Guidelines](https://github.com/FlysonBot/Mastermind/blob/main/CONTRIBUTING.md) to ensure a smooth and efficient collaboration process.

## License

Licensed under [MIT License]([/LICENSE](https://github.com/FlysonBot/Mastermind/blob/main/LICENSE)) by [@FlysonBot](https://github.com/FlysonBot).

## Questions?

If you have any questions, please feel free to leave them in the [Discussions](https://github.com/FlysonBot/Mastermind/discussions) or open up an [Issue](https://github.com/FlysonBot/Mastermind/issues).
