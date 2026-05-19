from urllib.parse import urlencode

from modules.utils import create_qr

def generate_upi_qr():

    upi_id = input("\nEnter UPI ID: ").strip()
    name = input("Enter Name: ").strip()
    amount = input("Enter Amount: ").strip()

    params = {"pa": upi_id}

    if name:
        params["pn"] = name

    if amount:
        params["am"] = amount

    data = f"upi://pay?{urlencode(params)}"

    filename = input("Enter filename: ")

    create_qr(data, filename)
