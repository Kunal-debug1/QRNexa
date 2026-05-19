from modules.utils import create_qr

def generate_text_qr():

    data = input("\nEnter text or URL: ")
    filename = input("Enter filename: ")

    create_qr(data, filename)