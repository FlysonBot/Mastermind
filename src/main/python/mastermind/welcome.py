import os
import shutil

from mastermind.gamemode import assisted, computer, human
from mastermind.rules import show_rules

_BANNER_WIDE = """
╔════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                        ║
║  ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██████╗   ║
║  ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗  ║
║  ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║  ██║  ║
║  ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║  ██║  ║
║  ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██████╔╝  ║
║  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝   ║
║                                                                                        ║
╚════════════════════════════════════════════════════════════════════════════════════════╝
"""

_BANNER_MEDIUM = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         ▗  ▖ ▗▖  ▄▄ ▄▄▄▖▗▄▄▖▗▄▄ ▗  ▖▗▄▄ ▗▖ ▖▗▄▖          ║
║         ▐▌▐▌ ▐▌ ▐▘ ▘ ▐  ▐   ▐ ▝▌▐▌▐▌ ▐  ▐▚ ▌▐ ▝▖         ║
║         ▐▐▌▌ ▌▐ ▝▙▄  ▐  ▐▄▄▖▐▄▄▘▐▐▌▌ ▐  ▐▐▖▌▐  ▌         ║
║         ▐▝▘▌ ▙▟   ▝▌ ▐  ▐   ▐ ▝▖▐▝▘▌ ▐  ▐ ▌▌▐  ▌         ║
║         ▐  ▌▐  ▌▝▄▟▘ ▐  ▐▄▄▖▐  ▘▐  ▌▗▟▄ ▐ ▐▌▐▄▞          ║
║                                                          ║
║              ·  ·  · SOLVE THE CODE ·  ·  ·              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

_BANNER_SMALL = """
╔══════════════════════════════════════╗
║                                      ║
║     ┏┳┓┏━┓┏━┓╺┳╸┏━╸┏━┓┏┳┓╻┏┓╻╺┳┓     ║
║     ┃┃┃┣━┫┗━┓ ┃ ┣╸ ┣┳┛┃┃┃┃┃┗┫ ┃┃     ║
║     ╹ ╹╹ ╹┗━┛ ╹ ┗━╸╹┗╸╹ ╹╹╹ ╹╺┻┛     ║
║                                      ║
╚══════════════════════════════════════╝
"""


def _terminal_width():
    cols_env = os.environ.get("COLUMNS")
    if cols_env and cols_env.isdigit():
        return int(cols_env)
    for fd in (1, 2, 0):  # stdout, stderr, stdin
        try:
            return os.get_terminal_size(fd).columns
        except OSError:
            pass
    return shutil.get_terminal_size().columns


def _banner():
    cols = _terminal_width()
    if cols >= 90:
        return _BANNER_WIDE
    if cols >= 60:
        return _BANNER_MEDIUM
    return _BANNER_SMALL

_MENU = """\
  1) Play  —  You guess the code
  2) Watch —  I solve the code
  3) Assist — You play in real life, I suggest guesses
  4) Rules —  How to play Mastermind
  5) Quit
"""


def welcome():
    print(_banner())

    while True:
        print(_MENU)
        choice = input("> ").strip()

        match choice:
            case "1":
                print()
                human.play()
            case "2":
                print()
                computer.play()
            case "3":
                print()
                assisted.play()
            case "4":
                show_rules()
            case "5":
                print("\nGoodbye!\n")
                break
            case _:
                print("  Please enter 1–5.\n")


if __name__ == "__main__":
    welcome()
