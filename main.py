from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from modules.text_qr import generate_text_qr
from modules.wifi_qr import generate_wifi_qr
from modules.whatsapp_qr import generate_whatsapp_qr
from modules.upi_qr import generate_upi_qr
from modules.contact_qr import generate_contact_qr

console = Console()

def banner():

    fig = Figlet(font='slant')

    title = fig.renderText('QuickQR')

    console.print(f"[bold cyan]{title}[/bold cyan]")

    console.print(
        Panel.fit(
            "[bold green]Professional QR Generator CLI[/bold green]\n"
            "[yellow]Built with Python[/yellow]",
            border_style="cyan"
        )
    )

def menu():

    while True:

        table = Table(title="QR Generator Menu", show_lines=True)

        table.add_column("Option", style="cyan", justify="center")
        table.add_column("Feature", style="green")

        table.add_row("1", "Text / URL QR")
        table.add_row("2", "WiFi QR")
        table.add_row("3", "WhatsApp QR")
        table.add_row("4", "UPI Payment QR")
        table.add_row("5", "Contact QR")
        table.add_row("6", "Exit")

        console.print(table)

        choice = console.input(
            "\n[bold yellow]Enter your choice:[/bold yellow] "
        )

        if choice == "1":
            generate_text_qr()

        elif choice == "2":
            generate_wifi_qr()

        elif choice == "3":
            generate_whatsapp_qr()

        elif choice == "4":
            generate_upi_qr()

        elif choice == "5":
            generate_contact_qr()

        elif choice == "6":
            console.print("\n[bold red]Exiting QuickQR...[/bold red]")
            break

        else:
            console.print(
                "\n[bold red]Invalid choice![/bold red]"
            )

if __name__ == "__main__":

    banner()

    menu()