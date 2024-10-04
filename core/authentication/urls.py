from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    ForgotPasswordAPI,
    LoginApi,
    LogoutApi,
    MeApi,
    RequestQRCodeApi,
    ResetPasswordAPI,
    ValidateOneTimePassword,
    VerifyOtpAPI,
)

app_name = "authentication"

urlpatterns: list[URLPattern] = [
    path("login/", LoginApi.as_view(), name="auth-login"),
    path("logout/", LogoutApi.as_view(), name="auth-logout"),
    path("me/", MeApi.as_view(), name="user-details"),
    path("qr-code/", RequestQRCodeApi.as_view(), name="auth-qr-code"),
    path("validate-otp/", ValidateOneTimePassword.as_view(), name="auth-validate-otp"),
    path("forgot-password/", ForgotPasswordAPI.as_view(), name="forgot-password"),
    path("verify-otp/", VerifyOtpAPI.as_view(), name="verify-otp"),
    path("reset-password/", ResetPasswordAPI.as_view(), name="reset-password"),
]
