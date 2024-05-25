from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.common.utils import get_list, get_object
from core.users.models import BaseUser, Guest, Member

from .serializers import (
    GuestDetailSerializer,
    GustListSerializer,
    MemberDetailSerializer,
    MemberListSerializer,
)


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
