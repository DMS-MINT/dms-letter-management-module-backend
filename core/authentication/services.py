import base64
from io import BytesIO

import pyotp
import qrcode
from rest_framework import status as http_status

from core.api.exceptions import APIError
from core.users.models import User


def setup_2fa(current_user: User):
    if current_user.otp_secret:
        secret_key = current_user.otp_secret
    else:
        secret_key = pyotp.random_base32()
        current_user.otp_secret = secret_key
        current_user.save()

    totp = pyotp.TOTP(secret_key)
    provisioning_uri = totp.provisioning_uri(name=current_user.full_name_am, issuer_name="DMS-MINT")

    qr = qrcode.make(provisioning_uri)
    buffer = BytesIO()
    qr.save(buffer)

    return base64.b64encode(buffer.getvalue()).decode()


def verify_otp(current_user: User, otp: str):
    totp = pyotp.TOTP(current_user.otp_secret)

    if not totp.verify(otp, valid_window=1):
        raise APIError(
            error_code="INVALID_OTP",
            status_code=http_status.HTTP_400_BAD_REQUEST,
            message="Invalid OTP provided. Please check the OTP and try again.",
            extra={"otp_error": "The provided OTP is incorrect."},
        )

    return True
