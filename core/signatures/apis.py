from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.authentication.services import verify_otp
from core.signatures.models import Signature


class GetDefaultSignature(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        otp = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        e_signature = serializers.ImageField()

    def post(self, request):
        current_user = request.user

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            result = verify_otp(current_user=current_user, **input_serializer.validated_data)

            if not result:
                raise ValueError("Invalid OTP provided.")

            signature_instance = Signature.objects.get(user=current_user)

            output_serializer = self.OutputSerializer(signature_instance)

            return Response(data=output_serializer.data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
