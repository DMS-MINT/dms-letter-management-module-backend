from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebTokenView

from core.api.mixins import ApiAuthMixin
from core.authentication.services import auth_logout
from core.users.selectors import user_get_login_data


class UserJwtLoginApi(ObtainJSONWebTokenView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.status_code = status.HTTP_200_OK

        return response


class UserJwtLogoutApi(APIView):
    def post(self, request):
        auth_logout(request.user)

        response = Response()

        if settings.JWT_AUTH["JWT_AUTH_COOKIE"] is not None:
            response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        return response


class UserMeApi(APIView):
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


class SecureAPIView(ApiAuthMixin, APIView):
    def get(self, request):
        return Response({"message": "This is a secure endpoint."})
