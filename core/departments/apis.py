from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin

from .models import Department

class DepartmentListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        abbreviation_am = serializers.CharField()
        abbreviation_en = serializers.CharField()
        department_name_en= serializers.CharField()
        department_name_am= serializers.CharField()

    serializer_class = OutputSerializer

    def get(self, request) -> Response:
        contacts = Department.objects.all()
        try:
            output_serializer = self.OutputSerializer(contacts, many=True)

            response_data = {"departments": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)

