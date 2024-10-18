from rest_framework import serializers

from core.common.utils import inline_serializer


class UserListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name_en = serializers.CharField()
    full_name_am = serializers.CharField()
    job_title = inline_serializer(
        fields={
            "title_en": serializers.CharField(),
            "title_am": serializers.CharField(),
        },
    )
    department = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "abbreviation_en": serializers.CharField(),
            "abbreviation_am": serializers.CharField(),
        },
    )


class UserDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name_en = serializers.CharField()
    full_name_am = serializers.CharField()
    job_title = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "title_en": serializers.CharField(),
            "title_am": serializers.CharField(),
        },
    )
    department = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "department_name_en": serializers.CharField(),
            "department_name_am": serializers.CharField(),
        },
    )
    phone_number = serializers.IntegerField()
    email = serializers.EmailField()


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name_en = serializers.CharField()
    middle_name_en = serializers.CharField()
    last_name_en = serializers.CharField()
    first_name_am = serializers.CharField()
    middle_name_am = serializers.CharField()
    last_name_am = serializers.CharField()
    full_name_en = serializers.CharField()
    full_name_am = serializers.CharField()
    job_title = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "title_en": serializers.CharField(),
            "title_am": serializers.CharField(),
        },
    )
    department = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "department_name_en": serializers.CharField(),
            "department_name_am": serializers.CharField(),
            "abbreviation_en": serializers.CharField(),
            "abbreviation_am": serializers.CharField(),
            "description": serializers.CharField(),
            "contact_phone": serializers.IntegerField(),
            "contact_email": serializers.EmailField(),
        },
    )
    phone_number = serializers.IntegerField()
    email = serializers.EmailField()
    is_2fa_enabled = serializers.BooleanField()
    is_staff = serializers.BooleanField()
