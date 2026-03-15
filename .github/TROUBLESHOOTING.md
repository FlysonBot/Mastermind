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

You need Python 3.12 or higher. If you see an error or an older version, install Python using one of the following
methods:

- **Windows** / **Mac**: [Download and install Python](https://www.python.org/downloads/).
- **Linux** (Debian/Ubuntu):
  ```bash
  sudo apt update && sudo apt install python3
  ```
- **Android/Termux**:
  ```bash
  pkg install python
  ```

## 3. Python not found after installation

If you installed Python but the `python` command still isn't found, your system PATH may not include Python. Try these
steps:

- **Windows**: During installation, make sure to check **"Add Python to PATH"**. If you missed it, reinstall and enable
  that option.
- **Mac / Linux**: Try `python3` instead of `python`.

## 4. pip

Check that pip is available:

```bash
pip --version
```

If you get an error, try `pip3` instead. If neither works, run:

```bash
python -m ensurepip --upgrade
```

If that still doesn't work, reinstall Python (pip is included by default).

## 6. Java error on Android/Termux

If you're installing from Android/Termux, install the following first:

```bash
pkg install x11-repo sdl2 openjdk-21
```

## 7. Pointer tag crash on Android/Termux

If you see an error like `Pointer tag for 0x... was truncated` and the app aborts, this is a
known bug in openjdk-21 on Android and is not caused by this application. Simply restart the
app. If it happens frequently, try running `pkg upgrade openjdk-21` to get the latest patched
version.

## 8. Still having trouble?

Open an issue on [GitHub](https://github.com/FlysonBot/Mastermind/issues) and include the error message and your platform. We'll help you out.

In the meantime, you can always try the [online version on Google Colab](https://colab.research.google.com/github/FlysonBot/Mastermind/blob/main/examples/mastermind_in_colab.ipynb) — no installation required.
