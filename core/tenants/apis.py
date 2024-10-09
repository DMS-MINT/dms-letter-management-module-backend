from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import inline_serializer

from .models import Tenant
from .selectors import tenant_detail
from .services import tenant_create


class TenantDetailApi(ApiAuthMixin, APIView):
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

    def get(self, requests, tenant_id):
        try:
            tenant_instance = Tenant.objects.prefetch_related(
                "tenant_profile__address",
                "domains",
            ).get(
                id=tenant_id,
            )

            tenant_data = tenant_detail(tenant_instance=tenant_instance)

            output_serializer = self.serializer_class(tenant_data)

            response_data = {"tenant": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class TenantCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name_en = serializers.CharField()
        name_am = serializers.CharField()
        tenant_slug = serializers.SlugField()
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
        try:
            input_serializer = self.serializer_class(data=request.data)
            input_serializer.is_valid(raise_exception=True)

            organization_id = tenant_create(
                current_user=request.user,
                **input_serializer.validated_data,
            )

            tenant_instance = Tenant.objects.prefetch_related(
                "tenant_profile__address",
                "domains",
            ).get(
                id=organization_id,
            )

            tenant_data = tenant_detail(tenant_instance=tenant_instance)

            output_serializer = TenantDetailApi.serializer_class(tenant_data)

            response_data = {"tenant": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)
        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
