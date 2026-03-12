from mastermind.gamemode import assisted, computer, human
from mastermind.rules import show_rules
from mastermind.ui import console
from rich.prompt import Prompt
from rich.rule import Rule

_BANNER_WIDE = """\
╔════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                        ║
║  ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██████╗   ║
║  ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗  ║
║  ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║  ██║  ║
║  ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║  ██║  ║
║  ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██████╔╝  ║
║  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝   ║
║                                                                                        ║
╚════════════════════════════════════════════════════════════════════════════════════════╝\
"""

_BANNER_MEDIUM = """\
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
╚══════════════════════════════════════════════════════════╝\
"""

_BANNER_SMALL = """\
╔══════════════════════════════════════╗
║                                      ║
║     ┏┳┓┏━┓┏━┓╺┳╸┏━╸┏━┓┏┳┓╻┏┓╻╺┳┓     ║
║     ┃┃┃┣━┫┗━┓ ┃ ┣╸ ┣┳┛┃┃┃┃┃┗┫ ┃┃     ║
║     ╹ ╹╹ ╹┗━┛ ╹ ┗━╸╹┗╸╹ ╹╹╹ ╹╺┻┛     ║
║                                      ║
╚══════════════════════════════════════╝\
"""


def _banner():
    cols = console.width
    if cols >= 90:
        return _BANNER_WIDE
    if cols >= 60:
        return _BANNER_MEDIUM
    return _BANNER_SMALL


def welcome():
    while True:
        console.print(f"\n[bold cyan]{_banner()}[/bold cyan]\n")
        console.print(Rule("[dim]Main Menu[/dim]", style="dim"))
        console.print()
        console.print("  [bold]1)[/bold] Play   [dim]—  You guess the code[/dim]")
        console.print("  [bold]2)[/bold] Watch  [dim]—  I solve the code[/dim]")
        console.print(
            "  [bold]3)[/bold] Assist [dim]—  You play in real life, I suggest guesses[/dim]"
        )
        console.print("  [bold]4)[/bold] Rules  [dim]—  How to play Mastermind[/dim]")
        console.print("  [bold]5)[/bold] Quit")
        console.print()

        choice = Prompt.ask("[bold]>[/bold]", console=console).strip()

        match choice:
            case "1":
                console.print()
                human.play()
            case "2":
                console.print()
                computer.play()
            case "3":
                console.print()
                assisted.play()
            case "4":
                show_rules()
            case "5":
                console.print("\n[dim]Goodbye![/dim]\n")
                break
            case _:
                console.print("  [red]Please enter 1–5.[/red]\n")


if __name__ == "__main__":
    welcome()
