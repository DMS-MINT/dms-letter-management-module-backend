from rest_framework import serializers

from core.common.utils import inline_serializer


class TenantSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name_en = serializers.CharField()
    name_am = serializers.CharField()

    slug = serializers.SlugField()

    domains = inline_serializer(
        many=True,
        fields={
            "domain": serializers.CharField(),
            "is_primary": serializers.BooleanField(),
        },
    )

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class TenantProfileSerializer(serializers.Serializer):
    bio = serializers.CharField()
    contact_phone = serializers.IntegerField()
    contact_email = serializers.EmailField()
    address = inline_serializer(
        fields={
            "city_en": serializers.CharField(),
            "city_am": serializers.CharField(),
        },
    )
    postal_code = serializers.IntegerField()


class TenantSettingSerializer(serializers.Serializer):
    auto_ref_number_letters = serializers.BooleanField()
    auto_date_letters = serializers.BooleanField()
