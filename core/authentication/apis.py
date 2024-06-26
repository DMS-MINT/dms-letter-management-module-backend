from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin

from .selectors import user_get_login_data

LOGOUT_HRF = "api/auth/logout/"


class LoginApi(APIView):
    """
    Following https://docs.djangoproject.com/en/5.0/topics/auth/default/#how-to-log-a-user-in
    """

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

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
            return Response({"message": "An unexpected error occurred", "extra": {"details": str(e)}}, status=500)


class GetUserSignature(ApiAuthMixin, APIView):
    def post(self, request):
        password = request.data.get("password")
        user = authenticate(username=request.user.email, password=password)
        if user is not None:
            signature_image_url = "/media/letters/signatures/default/signature_2.png"

            return Response(
                data={"message": "Verification successful", "signature_image": signature_image_url},
                status=status.HTTP_200_OK,
            )

        return Response(data={"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
