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
from .serializers import TenantProfileSerializer, TenantSerializer, TenantSettingSerializer
from .services import tenant_create


class TenantDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(TenantSerializer):
        tenant_profile = TenantProfileSerializer()
        tenant_settings = TenantSettingSerializer()

    serializer_class = OutputSerializer

    def get(self, request, tenant_id):
        try:
            tenant_instance = Tenant.objects.prefetch_related(
                "tenant_profile__address",
                "tenant_settings",
                "domains",
            ).get(
                id=tenant_id,
            )

            output_serializer = self.OutputSerializer(tenant_instance)

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

            tenant_id = tenant_create(
                current_user=request.user,
                **input_serializer.validated_data,
            )

            tenant_instance = Tenant.objects.prefetch_related(
                "tenant_profile__address",
                "tenant_settings",
                "domains",
            ).get(
                id=tenant_id,
            )

            output_serializer = TenantDetailApi.OutputSerializer(tenant_instance)

            response_data = {"tenant": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)
        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
