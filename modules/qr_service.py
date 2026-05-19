from io import BytesIO
from pathlib import Path
from time import time
from urllib.parse import quote, urlencode
import re

import qrcode

OUTPUT_DIR = Path("output")
VALID_TYPES = {
    "text",
    "wifi",
    "whatsapp",
    "upi",
    "contact",
    "sms",
    "email",
    "phone",
}


def safe_filename(filename):
    name = re.sub(r"[^a-zA-Z0-9._-]+", "_", filename.strip())
    return name.strip("._") or "quickqr"


def escape_wifi(value):
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace(":", "\\:")
    )


def escape_vcard(value):
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def build_payload(qr_type, values):
    if qr_type not in VALID_TYPES:
        raise ValueError("Unsupported QR type.")

    if qr_type == "wifi":
        ssid = values.get("ssid", "").strip()
        password = values.get("password", "")
        security = values.get("security", "WPA") or "WPA"
        if not ssid:
            raise ValueError("WiFi name is required.")
        return f"WIFI:T:{security};S:{escape_wifi(ssid)};P:{escape_wifi(password)};;"

    if qr_type == "whatsapp":
        phone = "".join(char for char in values.get("phone", "") if char.isdigit())
        message = values.get("message", "").strip()
        if not phone:
            raise ValueError("Phone number is required.")
        payload = f"https://wa.me/{phone}"
        if message:
            payload = f"{payload}?text={quote(message)}"
        return payload

    if qr_type == "upi":
        upi_id = values.get("upiId", "").strip()
        if not upi_id:
            raise ValueError("UPI ID is required.")
        params = {"pa": upi_id}
        if values.get("name", "").strip():
            params["pn"] = values["name"].strip()
        if values.get("amount", "").strip():
            params["am"] = values["amount"].strip()
        return f"upi://pay?{urlencode(params)}"

    if qr_type == "sms":
        phone = "".join(char for char in values.get("phone", "") if char.isdigit() or char == "+")
        message = values.get("message", "").strip()
        if not phone:
            raise ValueError("Phone number is required.")
        payload = f"SMSTO:{phone}"
        if message:
            payload = f"{payload}:{message}"
        return payload

    if qr_type == "email":
        address = values.get("email", "").strip()
        if not address:
            raise ValueError("Email address is required.")
        params = {}
        if values.get("subject", "").strip():
            params["subject"] = values["subject"].strip()
        if values.get("body", "").strip():
            params["body"] = values["body"].strip()
        query = urlencode(params)
        return f"mailto:{address}{'?' + query if query else ''}"

    if qr_type == "phone":
        phone = "".join(char for char in values.get("phone", "") if char.isdigit() or char == "+")
        if not phone:
            raise ValueError("Phone number is required.")
        return f"tel:{phone}"

    if qr_type == "contact":
        name = values.get("name", "").strip()
        phone = values.get("phone", "").strip()
        email = values.get("email", "").strip()
        if not any([name, phone, email]):
            raise ValueError("At least one contact field is required.")

        lines = ["BEGIN:VCARD", "VERSION:3.0"]
        if name:
            lines.append(f"FN:{escape_vcard(name)}")
        if phone:
            lines.append(f"TEL:{escape_vcard(phone)}")
        if email:
            lines.append(f"EMAIL:{escape_vcard(email)}")
        lines.append("END:VCARD")
        return "\n".join(lines)

    text = values.get("text", "").strip()
    if not text:
        raise ValueError("Text or URL is required.")
    return text


def make_qr_image(payload, fill_color="#101828", back_color="#ffffff", box_size=10):
    size = min(15, max(5, int(box_size)))
    qr = qrcode.QRCode(
        version=None,
        box_size=size,
        border=4,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill_color, back_color=back_color)


def save_qr(
    payload,
    filename,
    fill_color="#101828",
    back_color="#ffffff",
    box_size=10,
    output_dir=OUTPUT_DIR,
):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    image = make_qr_image(payload, fill_color, back_color, box_size)
    stem = safe_filename(filename) if filename else f"quickqr_{int(time() * 1000)}"
    path = output_path / f"{stem}.png"
    image.save(path)
    return path


def qr_png_bytes(payload, fill_color="#101828", back_color="#ffffff", box_size=10):
    image = make_qr_image(payload, fill_color, back_color, box_size)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
