from rest_framework import serializers

from core.departments.serializers import DepartmentSerializer, JobTitleSerializer


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()


class UserListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name_en = serializers.CharField(source="user_profile.full_name_en")
    full_name_am = serializers.CharField(source="user_profile.full_name_am")
    job_title = JobTitleSerializer(source="user_profile.job_title")


class UserDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name_en = serializers.CharField(source="user_profile.full_name_en")
    full_name_am = serializers.CharField(source="user_profile.full_name_am")
    job_title = JobTitleSerializer(source="user_profile.job_title")
    department = DepartmentSerializer(source="user_profile.department")
    phone_number = serializers.IntegerField()
    email = serializers.EmailField()


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    first_name_en = serializers.CharField(source="user_profile.first_name_en")
    middle_name_en = serializers.CharField(source="user_profile.middle_name_en")
    last_name_en = serializers.CharField(source="user_profile.last_name_en")
    first_name_am = serializers.CharField(source="user_profile.first_name_am")
    middle_name_am = serializers.CharField(source="user_profile.middle_name_am")
    last_name_am = serializers.CharField(source="user_profile.last_name_am")
    job_title = JobTitleSerializer(source="user_profile.job_title")
    department = DepartmentSerializer(source="user_profile.department")
    phone_number = serializers.CharField(source="user_profile.phone_number")
    is_staff = serializers.BooleanField()
    is_2fa_enabled = serializers.BooleanField(source="user_settings.is_2fa_enabled")
