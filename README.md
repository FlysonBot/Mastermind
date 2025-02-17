<p align="center">
<img src="https://raw.githubusercontent.com/FlysonBot/Mastermind/main/docs/source/_static/Mastermind Logo.svg" width="350">
</p>

| **Testing:** | [![Testing Status](https://img.shields.io/github/actions/workflow/status/FlysonBot/Mastermind/coverage.yaml?label=test)](https://github.com/FlysonBot/Mastermind/actions/workflows/coverage.yaml) [![Test Coverage](https://coveralls.io/repos/github/FlysonBot/Mastermind/badge.svg?branch=main)](https://coveralls.io/github/FlysonBot/Mastermind?branch=main) [![Docs Deploy Status](https://img.shields.io/github/actions/workflow/status/FlysonBot/Mastermind/deploy_sphinx.yaml?label=docs)](https://flysonbot.github.io/Mastermind/) [![CodeFactor](https://www.codefactor.io/repository/github/flysonbot/mastermind/badge/main)](https://www.codefactor.io/repository/github/flysonbot/mastermind/overview/main) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/af7ee6c4fbc945f88a41ef8edbea682d)](https://app.codacy.com/gh/FlysonBot/Mastermind/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)|
| --- | :-: |
| **Version:** | [![GitHub tag](https://img.shields.io/github/tag/FlysonBot/Mastermind?include_prereleases=&sort=semver&color=blue)](https://github.com/FlysonBot/Mastermind/tags) [![GitHub Release](https://img.shields.io/github/v/release/FlysonBot/Mastermind?include_prereleases)](https://github.com/FlysonBot/Mastermind/releases) [![Python Version](https://img.shields.io/pypi/pyversions/mastermind-ai)](https://www.python.org/downloads/) [![PyPI - Version](https://img.shields.io/pypi/v/mastermind-ai)](https://pypi.org/project/mastermind-ai/) |
| **Activity:** | [![Opened Issue Count](https://img.shields.io/github/issues/FlysonBot/Mastermind?color=teal)](<https://github.com/FlysonBot/Mastermind/issues>) [![Closed Issue Count](https://img.shields.io/github/issues-closed/FlysonBot/Mastermind?color=teal)](https://github.com/FlysonBot/Mastermind/issues?q=is%3Aissue+is%3Aclosed) [![Closed PR Count](https://img.shields.io/github/issues-pr-closed/FlysonBot/Mastermind?color=teal)](https://github.com/FlysonBot/Mastermind/pulls?q=is%3Apr+is%3Aclosed) [![PyPI - Downloads](https://img.shields.io/pypi/dw/mastermind-ai)](https://pypi.org/project/mastermind-ai/) |
| **Meta:** | [![GitHub License](https://img.shields.io/github/license/FlysonBot/Mastermind)](https://github.com/FlysonBot/Mastermind/blob/main/LICENSE) ![PyPI Status](https://img.shields.io/pypi/status/mastermind-ai) ![Repo Size](https://img.shields.io/github/repo-size/FlysonBot/Mastermind) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/FlysonBot/Mastermind/main.svg)](https://results.pre-commit.ci/latest/github/FlysonBot/Mastermind/main) |

> [!NOTE]
> Update: This repo is not being actively maintaned. To see the latest code, please visit the new-version branch.

> [!NOTE]
> This repo is currently still under development. Currently there is a beta version that have the basic simulation feature finished. If you encountered any issue, please open up an issue and let me know! I will try to fix them as soon as possible.

**Links:**

- [Documentation](https://flysonbot.github.io/Mastermind/)
- [Source Code](https://github.com/FlysonBot/Mastermind)
- [Releases](https://github.com/FlysonBot/Mastermind/releases)
- [Bug Reports](https://github.com/FlysonBot/Mastermind/issues)
- [Changelog](https://github.com/FlysonBot/Mastermind/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/FlysonBot/Mastermind/blob/main/.github/CONTRIBUTING.md)
- [Code of Conduct](https://github.com/FlysonBot/Mastermind/blob/main/.github/CODE_OF_CONDUCT.md)
- [Play Online on Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/examples/mastermind_in_colab.ipynb)

# Mastermind

> This is a python implementation of the classic puzzle game Mastermind. It simulates the game and allow you to play with either another human being (sits next to you) or the computer, with a AI Solver build-in (still under development). You can install this game with pip or try it out in your browser with [Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/examples/mastermind_in_colab.ipynb).

## What is Mastermind?

Mastermind is a code-breaking game for two players. The first player (the code-setter) creates a secret code, which the second player (the code-cracker) tries to guess. The code-cracker has a limited number of attempts to guess the code correctly. After each guess, the code-setter provides feedback to the code-cracker, indicating how many dots have the right color and are in the right place, and how many are the right color but in the wrong place. The code-cracker uses this feedback to refine their guesses until they correctly guess the code or run out of attempts.

## Contribution Wanted!!!

Currently the project only has 1 contributor, me, and I'm getting busy on schoolwork. Please come and contribtue! You don't need to know how to code to contribute. Simple open up [issues](https://github.com/FlysonBot/Mastermind/issues) or [discussion](https://github.com/FlysonBot/Mastermind/discussions) when you found bugs or have some suggestion to the project.

If you want to contribute to the code, feel free to fork and submit pull request! Try to follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style when writing commit message. Any help is appreciated! To get started, you can take a look at the issues labeled as [good first issue](https://github.com/FlysonBot/Mastermind/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) which contain a list of tasks that are easy to do that can help you get started with contributing to the project!

## Getting Started

### Prerequisites

To run this project, you must have the following installed (installation guide below):

- Python 3.10 (or higher)
- pip (comes with Python, needed to install the project as a library)

Or alternatively you can run this program in your browser with [Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/examples/mastermind_in_colab.ipynb)

### Installation Guide

1. Install [Python 3.10+](https://www.python.org/downloads/) if you have not already.

2. Install this the latest python release using pip in your terminal:

    ```bash
    pip install mastermind-ai
    ```

3. Run the program with the following command:

    ```bash
    mastermind
    ```

4. Enjoy!

> [!TIP]
> If the above does not work, try the troubleshooting guide below.

### Troubleshooting

If you encounter any issues during installation, please check the following:

1. Do you have trouble finding your terminal?

    - For windows users, press `Ctrl + R` and type `cmd` and press enter.
    - For mac users, press `Cmd + Space` and type `terminal` and press enter.
    - For linux users, press `Ctrl + Alt + T`.

2. Do you have the correct version of `python` installed? Check with the following command:

    ```bash
    python --version
    ```

    If you get an error, you need to install python.
    If your python version is lower than 3.10, you need to upgrade your python version.

3. Do you have `pip` installed properly? Check with the following command:

    ```bash
    pip --version
    ```

    If you get an error, you need to install `pip`.

4. Did you encountered an error associated with installing the dependencies of this project? Try installing the dependencies manually using the following command:

    ```bash
    pip install pandas
    ```

    If you get an error, the dependencies does not work on your machine. You will have to find your own way to install the dependencies.

5. If you are still having trouble, please feel free to open up an issue [here](https://github.com/FlysonBot/Mastermind/issues), and we will try to help you out. Or alternatively you can run the program in your [browser](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/examples/mastermind_in_colab.ipynb)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

All contributors must adhere to the [Contributor Covenant Code of Conduct](https://github.com/FlysonBot/Mastermind/blob/main/.github/CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive environment for all contributors.

To contribute to the code directly, you must also follow the [Contributing Guidelines](https://github.com/FlysonBot/Mastermind/blob/main/.github/CONTRIBUTING.md) to ensure a smooth and efficient collaboration process.

## License

Licensed under [MIT License](https://github.com/FlysonBot/Mastermind/blob/main/LICENSE) by [@FlysonBot](https://github.com/FlysonBot).

## Questions?

If you have any questions, please feel free to leave them in the [Discussions](https://github.com/FlysonBot/Mastermind/discussions) or open up an [Issue](https://github.com/FlysonBot/Mastermind/issues).
