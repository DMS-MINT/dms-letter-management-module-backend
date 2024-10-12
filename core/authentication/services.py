import base64
from io import BytesIO
from venv import logger
from core.emails.services import email_send_type
import pyotp
import qrcode
from django.contrib.auth.hashers import make_password
from rest_framework import status as http_status

from core.api.exceptions import APIError
from core.emails.tasks import email_send
from core.users.models import User


def create_user(
    *,
    email: str,
    password: str,
    is_staff: bool = False,
):
    return User.objects.create_user(
        email,
        password,
        is_staff=is_staff,
    )


def create_superuser(
    *,
    email: str,
    password: str,
):
    return User.objects.create_superuser(email, password)


def setup_2fa(current_user: User):
    if current_user.otp_secret:
        secret_key = current_user.otp_secret
    else:
        secret_key = pyotp.random_base32()
        current_user.otp_secret = secret_key
        current_user.save()

    totp = pyotp.TOTP(secret_key)
    provisioning_uri = totp.provisioning_uri(name=current_user.user_profile.full_name_am, issuer_name="DMS")

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


def generate_reset_otp(user):
    totp = pyotp.TOTP(user.otp_secret, interval=900)
    otp = totp.now()

    try:
        user.email
        name = user.first_name_en + " " + user.middle_name_en
        email_send_type(user.email, "OTP Verification", "otp", context={"otp_code": otp, "recipient_name": name})
        logger.info("OTP sent successfully to %s", user.email)

    except Exception as e:
        raise e


def verify_otp_reset(current_user: User, otp: str):
    totp = pyotp.TOTP(current_user.otp_secret, interval=900)

    if not totp.verify(otp, valid_window=1):
        raise APIError(
            error_code="INVALID_OTP",
            status_code=http_status.HTTP_400_BAD_REQUEST,
            message="Invalid OTP provided. Please check the OTP and try again.",
            extra={"otp_error": "The provided OTP is incorrect."},
        )

    return True


def reset_user_password(user: User, new_password: str):
    otp_secret = pyotp.random_base32()
    user.password = make_password(new_password)
    user.otp_secret = otp_secret
    user.user_settings.is_2fa_enabled = False
    user.save()
