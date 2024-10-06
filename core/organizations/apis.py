from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object, inline_serializer

from .models import Organization
from .selectors import organization_detail
from .services import create_organization, update_organization


class OrganizationDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name_en = serializers.CharField()
        name_am = serializers.CharField()
        domains = inline_serializer(
            many=True,
            fields={
                "id": serializers.UUIDField(),
                "domain": serializers.CharField(),
                "is_primary": serializers.BooleanField(),
            },
        )
        bio = serializers.CharField(default=None)
        contact_phone = serializers.IntegerField(default=None)
        contact_email = serializers.EmailField(default=None)
        address = inline_serializer(
            default=None,
            fields={
                "city_en": serializers.CharField(),
                "city_am": serializers.CharField(),
            },
        )
        postal_code = serializers.IntegerField(default=None)
        logo = serializers.ImageField(default=None)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    serializer_class = OutputSerializer

    def get(self, requests, organization_id):
        try:
            organization_instance = Organization.objects.prefetch_related(
                "organization_profile__address",
                "domains",
            ).get(
                id=organization_id,
            )

            organization_data = organization_detail(organization_instance=organization_instance)

            output_serializer = self.serializer_class(organization_data)

            response_data = {"organization": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class OrganizationCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name_en = serializers.CharField()
        name_am = serializers.CharField()
        organization_slug = serializers.SlugField()
        bio = serializers.CharField(required=False)
        address = inline_serializer(
            fields={
                "city_en": serializers.CharField(),
                "city_am": serializers.CharField(),
            },
        )
        contact_phone = serializers.IntegerField(required=False)
        contact_email = serializers.EmailField(required=False)
        postal_code = serializers.IntegerField(required=False)
        logo = Base64ImageField(required=False)

    serializer_class = InputSerializer

    def post(self, request):
        input_serializer = self.serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            organization_instance, _ = create_organization(
                current_user=request.user,
                **input_serializer.validated_data,
            )

            output_serializer = OrganizationDetailApi.OutputSerializer(organization_instance)

            response_data = {"organization": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)
        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class OrganizationUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name_en = serializers.CharField(max_length=255)
        name_am = serializers.CharField(max_length=255)
        bio = serializers.CharField()
        address = inline_serializer(
            fields={
                "city_en": serializers.CharField(max_length=100),
                "city_am": serializers.CharField(max_length=100),
            },
        )
        contact_phone = serializers.IntegerField()
        contact_email = serializers.EmailField()
        postal_code = serializers.IntegerField()
        logo = Base64ImageField()

    serializer_class = InputSerializer

    def put(self, request, organization_id):
        organization_instance = get_object(Organization, id=organization_id)

        input_serializer = self.serializer_class(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            organization_instance = Organization.objects.prefetch_related(
                "organization_profile__address",
            ).get(
                id=organization_id,
            )

            organization_instance = update_organization(
                organization_instance=organization_instance,
                **input_serializer.validated_data,
            )

            output_serializer = OrganizationDetailApi.OutputSerializer(organization_instance)

            response_data = {"organization": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
