from mastermind.rules import show_rules
from mastermind.gamemode import human, computer, assisted


_BANNER = """
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

_MENU = """\
  1) Play  —  You guess the code
  2) Watch —  I solve the code
  3) Assist — You play in real life, I suggest guesses
  4) Rules —  How to play Mastermind
  5) Quit
"""


def welcome():
    print(_BANNER)

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
