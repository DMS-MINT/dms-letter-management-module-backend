from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.authentication.services import setup_2fa, verify_otp
from core.signatures.models import Signature

from .selectors import user_get_login_data

LOGOUT_HRF = "api/auth/logout/"


class LoginApi(APIView):
    """
    Following https://docs.djangoproject.com/en/5.0/topics/auth/default/#how-to-log-a-user-in
    """

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    serializer_class = InputSerializer

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is None:
            raise AuthenticationFailed("Invalid login credentials. Please try again or contact support.")

        login(request, user)

        session_key = request.session.session_key

        response_data = {
            "action": [
                {
                    "name": "Logout",
                    "hrf": LOGOUT_HRF,
                    "method": "POST",
                },
            ],
            "session": session_key,
        }

        return Response(data=response_data)


class LogoutApi(ApiAuthMixin, APIView):
    def get(self, request):
        logout(request)

        return Response(data={"message": "The user has been logged out successfully."})


class MeApi(ApiAuthMixin, APIView):
    def get(self, request):
        try:
            data = user_get_login_data(current_user=request.user)

            response_data = {
                "action": [
                    {
                        "name": "User Listing",
                        "hrf": LOGOUT_HRF,
                        "method": "GET",
                    },
                ],
                "data": data,
            }

            return Response(data=response_data)

        except NotFound as e:
            raise NotFound(e)
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred", "extra": {"details": str(e)}},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RequestQRCodeApi(ApiAuthMixin, APIView):
    def post(self, request):
        current_user = request.user

        try:
            qr_code_image = setup_2fa(current_user=current_user)

            response_data = {"qr_code_image": qr_code_image}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class ValidateOneTimePassword(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        otp = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        e_signature = serializers.ImageField()

    def post(self, request):
        current_user = request.user

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            result = verify_otp(current_user=current_user, **input_serializer.validated_data)

            if not result:
                raise ValidationError({"otp": "The provided OTP is invalid."})

            signature_instance = Signature.objects.get(user=current_user)

            output_serializer = self.OutputSerializer(signature_instance)

            return Response(data=output_serializer.data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
