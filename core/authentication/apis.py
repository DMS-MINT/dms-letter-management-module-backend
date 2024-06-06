from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.users.selectors import user_get_login_data


class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        pass


class LogoutApi(APIView):
    def post(self, request):
        pass


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
