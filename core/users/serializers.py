from rest_framework import serializers

from core.common.utils import inline_serializer


class UserListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
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
            "department_name_en": serializers.CharField(),
            "department_name_am": serializers.CharField(),
        },
    )
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()


class UserDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()

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
            "title_en": serializers.CharField(),
            "title_am": serializers.CharField(),
        },
    )
    department = inline_serializer(
        fields={
            "department_name_en": serializers.CharField(),
            "department_name_am": serializers.CharField(),
        },
    )
    phone_number = serializers.IntegerField()

    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()


class CurrentUserSerializer(UserDetailSerializer):
    is_2fa_enabled = serializers.BooleanField(source="user_settings.is_2fa_enabled", default=False)
