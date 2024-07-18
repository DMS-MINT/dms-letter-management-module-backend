from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin


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
