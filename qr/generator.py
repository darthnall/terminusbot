from qrcode import QRCode
from qrcode import constants

def create_qr(imei: str) -> bool:
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'https://terminusgps.com/register?imei={imei}')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("test.png")
    return True
