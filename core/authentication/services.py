import base64
from io import BytesIO

import pyotp
import qrcode

from core.users.models import Member


def setup_2fa(current_user: Member):
    if current_user.otp_secret:
        secret_key = current_user.otp_secret
    else:
        secret_key = pyotp.random_base32()
        current_user.otp_secret = secret_key
        current_user.save()

    totp = pyotp.TOTP(secret_key)
    provisioning_uri = totp.provisioning_uri(name=current_user.full_name, issuer_name="DMS-MINT")

    qr = qrcode.make(provisioning_uri)
    buffer = BytesIO()
    qr.save(buffer)

    return base64.b64encode(buffer.getvalue()).decode()


def verify_otp(current_user: Member, otp: int):
    totp = pyotp.TOTP(current_user.otp_secret)

    if totp.verify(otp):
        return True

    return False
