from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object

from .models import Department
from .services import department_create, department_update


class DepartmentListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        department_name_en = serializers.CharField(max_length=255)
        department_name_am = serializers.CharField(max_length=255)
        abbreviation_en = serializers.CharField(max_length=3)
        abbreviation_am = serializers.CharField(max_length=3)

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            departments = Department.objects.all()

            output_serializer = self.serializer_class(departments, many=True)

            response_data = {"departments": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class DepartmentDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        department_name_en = serializers.CharField(max_length=255)
        department_name_am = serializers.CharField(max_length=255)
        abbreviation_en = serializers.CharField(max_length=3)
        abbreviation_am = serializers.CharField(max_length=3)
        description = serializers.CharField(default=None)
        contact_phone = serializers.IntegerField(default=None)
        contact_email = serializers.EmailField(default=None)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    serializer_class = OutputSerializer

    def get(self, request, department_id):
        department_instance = get_object(Department, id=department_id)

        try:
            output_serializer = self.serializer_class(department_instance)

            response_data = {"department": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class DepartmentCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        department_name_en = serializers.CharField(max_length=255)
        department_name_am = serializers.CharField(max_length=255)
        abbreviation_en = serializers.CharField(max_length=3)
        abbreviation_am = serializers.CharField(max_length=3)
        description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
        contact_phone = serializers.IntegerField(required=False, allow_null=True)
        contact_email = serializers.EmailField(required=False, allow_null=True)

    serializer_class = InputSerializer

    def post(self, request):
        input_serializer = self.serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            department_instance = department_create(**input_serializer.validated_data)

            output_serializer = DepartmentDetailApi.OutputSerializer(department_instance)

            response_data = {"department": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class DepartmentUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        department_name_en = serializers.CharField(max_length=255)
        department_name_am = serializers.CharField(max_length=255)
        abbreviation_en = serializers.CharField(max_length=3)
        abbreviation_am = serializers.CharField(max_length=3)
        description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
        contact_phone = serializers.IntegerField(required=False, allow_null=True)
        contact_email = serializers.EmailField(required=False, allow_null=True)

    serializer_class = InputSerializer

    def put(self, request, department_id):
        department_instance = get_object(Department, id=department_id)
        input_serializer = self.serializer_class(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            department_instance = department_update(
                department_instance=department_instance,
                **input_serializer.validated_data,
            )

            output_serializer = DepartmentDetailApi.OutputSerializer(department_instance)

            response_data = {"organization": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class DepartmentDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, department_id):
        department_instance = get_object(Department, id=department_id)

        try:
            department_instance.delete()

            response_data = {"message": "Department removed from your list successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)
