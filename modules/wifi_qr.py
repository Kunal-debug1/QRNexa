from modules.utils import create_qr


def escape_wifi(value):
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace(":", "\\:")
    )


def generate_wifi_qr():

    ssid = input("\nEnter WiFi Name (SSID): ").strip()
    password = input("Enter WiFi Password: ")

    data = f"WIFI:T:WPA;S:{escape_wifi(ssid)};P:{escape_wifi(password)};;"

    filename = input("Enter filename: ")

    create_qr(data, filename)
