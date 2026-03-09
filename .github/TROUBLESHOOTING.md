# Troubleshooting

If you encounter issues installing or running Mastermind, check the following.

## 1. Finding your terminal

- **Windows**: Press `Ctrl + R`, type `cmd`, and press Enter.
- **Mac**: Press `Cmd + Space`, type `terminal`, and press Enter.
- **Linux**: Press `Ctrl + Alt + T`.

## 2. Python version

Check your Python version:

```bash
python --version
```

You need Python 3.12 or higher. If you see an error or an older version, [download and install Python](https://www.python.org/downloads/).

## 3. pip

Check that pip is available:

```bash
pip --version
```

If you get an error, reinstall Python (pip is included by default).

## 4. Java error on Android/Termux

If you see a Java-related error on Android/Termux, install OpenJDK 21 first:

```bash
pkg install openjdk-21
```

Java is bundled for Linux, Windows, and macOS — this step is only needed on Termux.

## 5. Still having trouble?

Open an issue on [GitHub](https://github.com/FlysonBot/Mastermind/issues) and include the error message and your platform. We'll help you out.

In the meantime, you can always try the [online version on Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/examples/mastermind_in_colab.ipynb) — no installation required.
