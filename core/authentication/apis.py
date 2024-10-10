from venv import logger

from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.exceptions import APIError
from core.api.mixins import ApiAuthMixin
from core.authentication.services import (
    generate_reset_otp,
    reset_user_password,
    setup_2fa,
    verify_otp,
)
from core.common.utils import get_object
from core.tenants.selectors import list_user_tenants
from core.user_management.selectors import user_profile_details
from core.users.models import User
from core.users.serializers import CurrentUserSerializer

from .services import create_user


class SignUpApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    serializer_class = InputSerializer

    def post(self, request):
        try:
            input_serializer = self.serializer_class(data=request.data)
            input_serializer.is_valid(raise_exception=True)

            user_instance = create_user(**input_serializer.validated_data, is_staff=True)

            response_data = {
                "message": "Your account has been successfully created.",
                "email": user_instance.email,
            }

            return Response(data=response_data)

        except ValidationError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LoginApi(APIView):
    """
    Following https://docs.djangoproject.com/en/5.0/topics/auth/default/#how-to-log-a-user-in
    """

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    serializer_class = InputSerializer

    def post(self, request):
        try:
            serializer = self.InputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = authenticate(request, **serializer.validated_data)

            if user is None:
                raise AuthenticationFailed("Invalid login credentials. Please try again or contact support.")

            login(request, user)

            session_key = request.session.session_key

            tenants = user.tenants.all()
            user_tenants = list_user_tenants(user_id=user.id, tenants=tenants)

            response_data = {
                "session": session_key,
                "tenants": user_tenants,
            }

            return Response(data=response_data)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LogoutApi(ApiAuthMixin, APIView):
    def get(self, request):
        logout(request)

        return Response(data={"message": "The user has been logged out successfully."})


class MeApi(ApiAuthMixin, APIView):
    serializer_class = CurrentUserSerializer

    def get(self, request):
        try:
            user_instance = User.objects.get(id=request.user.id)

            user_profile = user_profile_details(user_instance=user_instance)

            output_serializer = CurrentUserSerializer(user_profile)

            response_data = {"my_profile": output_serializer.data}

            return Response(data=response_data)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


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
        otp = serializers.CharField()

    def post(self, request):
        current_user = request.user

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            verify_otp(current_user=current_user, **input_serializer.validated_data)

            current_user.is_2fa_enabled = True
            current_user.save()

            response_data = {"message": "OTP verified successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class ForgotPasswordAPI(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        logger.info("Received request for forgot password.")
        try:
            serializer = self.InputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data["email"]
            logger.info("Processing password reset for email: %s", email)
            user = get_object(User, email=email)

            if user is None:
                logger.warning("No user found with email: %s", email)
                return Response({"message": "No user found with this email."}, status=http_status.HTTP_404_NOT_FOUND)

            try:
                # Generate and send OTP
                generate_reset_otp(user)
                logger.info("OTP successfully sent to email: %s", email)
                return Response({"message": "OTP has been sent to your email."}, status=http_status.HTTP_200_OK)
            except Exception as otp_error:
                logger.error("Error sending OTP: %s", str(otp_error))
                return Response(
                    {"error_code": "INTERNAL_SERVER_ERROR", "message": "Failed to send OTP."},
                    status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            logger.error("Unexpected error in ForgotPasswordAPI: %s", str(e), exc_info=True)
            return Response(
                {"error_code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred"},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyOtpAPI(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        otp = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        user = get_object(User, email=email)

        # Verify the OTP
        verify_otp(user, otp)

        return Response({"message": "OTP verified successfully."}, status=http_status.HTTP_200_OK)


class ResetPasswordAPI(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        new_password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        new_password = serializer.validated_data["new_password"]
        user = get_object(User, email=email)

        # Reset the user's password
        reset_user_password(user, new_password)

        return Response({"message": "Password reset successful."}, status=http_status.HTTP_200_OK)
