from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.api.mixins import ApiAuthMixin
from core.users.models import BaseUser, Guest, Member

from .selectors import user_get_suggestions
from .serializers import (
    GuestDetailSerializer,
    GustListSerializer,
    MemberDetailSerializer,
    MemberListSerializer,
)

GET_USERS_HRF = "api/users/"
GET_USER_HRF = "api/users/<uuid:user_id>/"


class UserListApi(ApiAuthMixin, APIView):
    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "user_type"
        model_serializer_mapping = {
            Member: MemberListSerializer,
            Guest: GustListSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    def get(self, request) -> Response:
        try:
            user = user_get_suggestions()
            serializer = self.OutputSerializer(user, many=True)

            response_data = {
                "action": [
                    {
                        "name": "User Details",
                        "hrf": GET_USER_HRF,
                        "method": "GET",
                    },
                ],
                "data": serializer.data,
            }

            return Response(data=response_data)

        except NotFound as e:
            raise NotFound({"message": str(e), "extra": {}}, status=404)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "extra": {"details": str(e)}}, status=500)


class UserDetailAPI(ApiAuthMixin, APIView):
    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "user_type"
        model_serializer_mapping = {
            Member: MemberDetailSerializer,
            Guest: GuestDetailSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    def get(self, request, user_id):
        try:
            user_instance = get_object_or_404(BaseUser, id=user_id)

            serializer = self.OutputSerializer(user_instance)

            response_data = {
                "action": [
                    {
                        "name": "User Listing",
                        "hrf": GET_USERS_HRF,
                        "method": "GET",
                    },
                ],
                "data": serializer.data,
            }

            return Response(data=response_data)

        except NotFound as e:
            raise NotFound(e)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "extra": {"details": str(e)}}, status=500)
