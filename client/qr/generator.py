from qrcode import QRCode
from qrcode import constants


def create_qr(imei: int) -> bool:
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    base = f"localhost"
    protocol = "http"
    port = 5000
    url = f"{protocol}://{base}:{port}/register?imei={imei}"

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{imei}.png")
    return True


if __name__ == "__main__":
    create_qr(867730053567180)
