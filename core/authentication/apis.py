from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.users.selectors import user_get_login_data

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

        data = user_get_login_data(user=user)
        session_key = request.session.session_key

        response_data = {
            "action": [
                {
                    "name": "Logout",
                    "hrf": LOGOUT_HRF,
                    "method": "POST",
                },
            ],
            "data": data,
            "session": session_key,
        }

        return Response(data=response_data)


class LogoutApi(ApiAuthMixin, APIView):
    def get(self, request):
        logout(request)

        return Response()

    def post(self, request):
        logout(request)

        return Response()
