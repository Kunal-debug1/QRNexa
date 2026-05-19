from urllib.parse import quote

from modules.utils import create_qr

def generate_whatsapp_qr():

    phone = "".join(
        char for char in input("\nEnter phone number with country code: ")
        if char.isdigit()
    )
    message = input("Enter WhatsApp message: ")

    data = f"https://wa.me/{phone}"

    if message.strip():
        data = f"{data}?text={quote(message.strip())}"

    filename = input("Enter filename: ")

    create_qr(data, filename)
