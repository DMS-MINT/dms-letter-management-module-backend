from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebTokenView

from core.api.mixins import ApiAuthMixin
from core.authentication.services import auth_logout
from core.users.selectors import user_get_login_data


class LoginApi(ObtainJSONWebTokenView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            token = response.data.get("token")

            response = JsonResponse({"token": token})

            response.set_cookie(
                key=settings.JWT_AUTH["JWT_AUTH_COOKIE"],
                value=token,
                httponly=True,
                secure=settings.JWT_AUTH["JWT_AUTH_COOKIE_SECURE"],
                samesite=settings.JWT_AUTH["JWT_AUTH_COOKIE_SAMESITE"],
                max_age=int(settings.JWT_EXPIRATION_DELTA_SECONDS),
            )
            response.status_code = status.HTTP_200_OK

        return response


class LogoutApi(APIView):
    def post(self, request):
        auth_logout(request.user)

        response = Response()

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        # if settings.JWT_AUTH["JWT_AUTH_COOKIE"] is not None:
        #     response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        return response


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        response_data = {
            "action": [
                {
                    "name": "Logout",
                    "hrf": "",
                    "method": "POST",
                },
                {
                    "name": "Update Profile",
                    "hrf": "",
                    "method": "PUT",
                },
            ],
            "data": data,
        }

        return Response(data=response_data)
