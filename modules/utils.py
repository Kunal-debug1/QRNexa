from rich.console import Console
from rich.panel import Panel

from modules.qr_service import save_qr, safe_filename

console = Console()


def read_box_size():
    try:
        box_size = int(console.input("[cyan]Enter QR size (5-15):[/cyan] "))
    except ValueError:
        return 10

    return min(15, max(5, box_size))


def create_qr(data, filename):
    fill_color = console.input("[cyan]Enter QR color:[/cyan] ").strip() or "black"
    bg_color = console.input("[cyan]Enter background color:[/cyan] ").strip() or "white"
    box_size = read_box_size()
    save_path = save_qr(data, safe_filename(filename), fill_color, bg_color, box_size)

    console.print(
        Panel.fit(
            f"[bold green]QR Code saved successfully![/bold green]\n\n"
            f"[yellow]Location:[/yellow] {save_path}",
            border_style="green",
        )
    )

    return save_path
