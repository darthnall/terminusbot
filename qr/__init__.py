from qrcode import QRCode
from qrcode import constants

if __name__ == "__main__":
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    imei = 1234235345
    qr.add_data(f'localhost:5000/register?imei={imei}')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("test.png")
