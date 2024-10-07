from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import HasTenantAccess
from core.common.utils import get_object

from .models import JobTitle
from .services import job_title_create, job_title_update


class JobTitleListApi(APIView):
    permission_classes = [IsAuthenticated, HasTenantAccess]

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title_en = serializers.CharField(max_length=255)
        title_am = serializers.CharField(max_length=255)

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            job_titles = JobTitle.objects.all()

            output_serializer = self.serializer_class(job_titles, many=True)

            response_data = {"job_titles": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class JobTitleDetailApi(APIView):
    permission_classes = [IsAuthenticated, HasTenantAccess]

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title_en = serializers.CharField(max_length=255)
        title_am = serializers.CharField(max_length=255)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    serializer_class = OutputSerializer

    def get(self, request, job_title_id):
        job_title_instance = get_object(JobTitle, id=job_title_id)

        try:
            output_serializer = self.serializer_class(job_title_instance)

            response_data = {"job_title": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class JobTitleCreateApi(APIView):
    permission_classes = [IsAuthenticated, HasTenantAccess]

    class InputSerializer(serializers.Serializer):
        title_en = serializers.CharField(max_length=255)
        title_am = serializers.CharField(max_length=255)

    serializer_class = InputSerializer

    def post(self, request):
        input_serializer = self.serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            job_title_instance = job_title_create(**input_serializer.validated_data)

            output_serializer = JobTitleDetailApi.OutputSerializer(job_title_instance)

            response_data = {"job_title": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class JobTitleUpdateApi(APIView):
    permission_classes = [IsAuthenticated, HasTenantAccess]

    class InputSerializer(serializers.Serializer):
        title_en = serializers.CharField(max_length=255)
        title_am = serializers.CharField(max_length=255)

    serializer_class = InputSerializer

    def put(self, request, job_title_id):
        job_title_instance = get_object(JobTitle, id=job_title_id)

        input_serializer = self.serializer_class(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            job_title_instance = job_title_update(
                job_title_instance=job_title_instance,
                **input_serializer.validated_data,
            )

            output_serializer = JobTitleDetailApi.OutputSerializer(job_title_instance)

            response_data = {"job_title": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class JobTitleDeleteApi(APIView):
    permission_classes = [IsAuthenticated, HasTenantAccess]

    def delete(self, request, job_title_id):
        job_title_instance = get_object(JobTitle, id=job_title_id)

        try:
            job_title_instance.delete()

            response_data = {"message": "JobTitle removed from your list successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)
