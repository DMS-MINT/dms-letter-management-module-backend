from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.authentication.services import setup_2fa, verify_otp

from .selectors import user_get_login_data


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
                "my_profile": data,
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

    def post(self, request):
        current_user = request.user

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            result = verify_otp(current_user=current_user, **input_serializer.validated_data)

            if not result:
                raise ValueError("Invalid OTP provided.")

            current_user.is_2fa_enabled = True
            current_user.save()

            response_data = {"message": "OTP verified successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
