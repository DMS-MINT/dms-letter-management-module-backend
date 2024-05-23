from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import Guest, Member


class GustListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class MemberListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name = serializers.CharField()
    job_title = serializers.CharField()


class GuestDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    postal_code = serializers.CharField()


class MemberDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.CharField()
    job_title = serializers.CharField()
    department = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    modified = serializers.DateTimeField()


class MemberCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class GuestCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField(required=False)
    address = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    postal_code = serializers.IntegerField(required=False)


class UserCreateSerializer(PolymorphicSerializer):
    resource_type_field_name = "user_type"
    model_serializer_mapping = {
        Member: MemberCreateSerializer,
        Guest: GuestCreateSerializer,
    }

    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()
