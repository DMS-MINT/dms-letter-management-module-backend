from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin

from .models import Enterprise


class EnterpriseListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name_en = serializers.CharField()
        name_am = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.IntegerField()
        address = serializers.CharField()
        postal_code = serializers.IntegerField()
        logo = serializers.ImageField()

    def get(self, request) -> Response:
        contacts = Enterprise.objects.all()
        try:
            output_serializer = self.OutputSerializer(contacts, many=True)

            response_data = {"enterprises": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
