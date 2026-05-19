from modules.utils import create_qr


def escape_vcard(value):
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def generate_contact_qr():

    name = input("\nEnter Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email: ").strip()

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
    ]

    if name:
        lines.append(f"FN:{escape_vcard(name)}")

    if phone:
        lines.append(f"TEL:{escape_vcard(phone)}")

    if email:
        lines.append(f"EMAIL:{escape_vcard(email)}")

    lines.append("END:VCARD")
    data = "\n".join(lines)

    filename = input("Enter filename: ")

    create_qr(data, filename)
