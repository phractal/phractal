import base64
import io
import qrcode


def gen_qrcode(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=1,
    )
    qr.make(fit=True)
    qr.add_data(text)
    img = qr.make_image()
    buf = io.BytesIO()
    img.save(buf, format='png')
    image_stream = buf.getvalue()
    base64_img = 'data:image/png;base64,' + base64.b64encode(image_stream).decode()
    return base64_img


if __name__ == '__main__':
    text1 = "123456"
    gen_qrcode(text1)
