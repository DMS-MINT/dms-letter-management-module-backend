from rest_framework import serializers

from core.common.utils import inline_serializer
from core.users.models import User


class MemberProfileSerializer(serializers.Serializer):
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


class MemberProfileDetailSerializer(serializers.Serializer):
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
        },
    )
    phone_number = serializers.IntegerField()


class MemberPermissionsSerializer(serializers.Serializer):
    is_admin = serializers.BooleanField()
    is_staff = serializers.BooleanField()


class MemberSettingsSerializer(serializers.Serializer):
    is_2fa_enabled = serializers.BooleanField()
    is_verified = serializers.BooleanField()


class MemberPreferencesSerializer(serializers.Serializer):
    pass


class MemberListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.SerializerMethodField()
    member_profile = MemberProfileSerializer()
    member_permissions = MemberPermissionsSerializer()

    def get_email(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.email


class MemberDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.SerializerMethodField()
    member_profile = MemberProfileDetailSerializer()
    member_permissions = MemberPermissionsSerializer()
    member_settings = MemberSettingsSerializer()

    def get_email(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.email
