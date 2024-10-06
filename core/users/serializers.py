from rest_framework import serializers

from core.departments.serializers import DepartmentSerializer, JobTitleSerializer


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()


class UserListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name_en = serializers.CharField(source="user_profile.full_name_en", default=None)
    full_name_am = serializers.CharField(source="user_profile.full_name_am", default=None)
    job_title = JobTitleSerializer(source="user_profile.job_title", default=None)
    department = DepartmentSerializer(source="user_profile.department", default=None)
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()


class UserDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name_en = serializers.CharField(source="user_profile.full_name_en", default=None)
    full_name_am = serializers.CharField(source="user_profile.full_name_am", default=None)
    job_title = JobTitleSerializer(source="user_profile.job_title", default=None)
    department = DepartmentSerializer(source="user_profile.department", default=None)
    phone_number = serializers.IntegerField(default=None)
    email = serializers.EmailField()


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()

    first_name_en = serializers.CharField(source="user_profile.first_name_en", default=None)
    middle_name_en = serializers.CharField(source="user_profile.middle_name_en", default=None)
    last_name_en = serializers.CharField(source="user_profile.last_name_en", default=None)

    first_name_am = serializers.CharField(source="user_profile.first_name_am", default=None)
    middle_name_am = serializers.CharField(source="user_profile.middle_name_am", default=None)
    last_name_am = serializers.CharField(source="user_profile.last_name_am", default=None)

    job_title = JobTitleSerializer(source="user_profile.job_title", default=None)
    department = DepartmentSerializer(source="user_profile.department", default=None)
    phone_number = serializers.CharField(source="user_profile.phone_number", default=None)

    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    is_2fa_enabled = serializers.BooleanField(source="user_settings.is_2fa_enabled", default=False)
