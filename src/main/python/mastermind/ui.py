from rich.console import Console

console = Console(width=min(Console().width, 90))


def pause():
    console.print("[dim]Press Enter to return to the menu...[/dim]", end="")
    input()
