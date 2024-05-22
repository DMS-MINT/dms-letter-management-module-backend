from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.common.utils import get_list, get_object
from core.users.models import BaseUser, Guest, Member


class GustListSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class MemberListSerializer(serializers.Serializer):
    id = serializers.CharField()
    full_name = serializers.CharField()
    job_title = serializers.CharField()


class UserListApi(APIView):
    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "user_type"
        model_serializer_mapping = {
            Member: MemberListSerializer,
            Guest: GustListSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    def get(self, request) -> Response:
        users = get_list(BaseUser)

        if users is None:
            return Response({"detail": "users not found"}, status=404)

        serializer = self.OutputSerializer(users, many=True)

        return Response(data=serializer.data)


class GuestDetailSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    postal_code = serializers.CharField()


class MemberDetailSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.CharField()
    job_title = serializers.CharField()
    department = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    modified = serializers.DateTimeField()


class UserDetailAPI(APIView):
    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "user_type"
        model_serializer_mapping = {
            Member: MemberDetailSerializer,
            Guest: GuestDetailSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    def get(self, request, user_id) -> Response:
        user_instance = get_object(BaseUser, id=user_id)

        if user_instance is None:
            return Response({"detail": "User not found"}, status=404)

        serializer = self.OutputSerializer(user_instance, many=False)

        return Response(data=serializer.data)
