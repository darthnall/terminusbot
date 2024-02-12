from qrcode import QRCode
from qrcode import constants

if __name__ == "__main__":
    qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
    )

    qr.add_data('https://hosting.wialon.com/login.html?user=Blake@terminusgps.com')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("Blake.png")
