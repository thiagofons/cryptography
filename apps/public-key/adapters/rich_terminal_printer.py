from model import ITerminalPrinter
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class RichTerminalPrinter(ITerminalPrinter):
    def __init__(self):
        self._console = Console()

    def print_title(self, text: str) -> None:
        styled_content = Text(text, style="bold cyan", justify="center")
        
        panel = Panel(
            styled_content, 
            border_style="cyan", 
            expand=True
        )
        self._console.print(panel)

    def print_step(self, label: str, value: str) -> None:
        self._console.print(f"[bold green]✔ {label}:[/bold green] [white]{value}[/white]")

    def print_alert(self, text: str) -> None:
        self._console.print(f"[bold yellow]⚠ {text}[/bold yellow]")
