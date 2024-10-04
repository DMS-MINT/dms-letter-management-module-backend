from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.users.models.user import User

from .selectors import user_get_users
from .serializers import UserDetailSerializer, UserListSerializer


class UserListApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        is_staff = serializers.BooleanField(required=False)

    serializer_class = UserListSerializer
    filter_class = FilterSerializer

    def get(self, request) -> Response:
        try:
            filter_serializer = self.FilterSerializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)

            user = user_get_users(current_user=request.user, filters=filter_serializer.validated_data)
            out_serializer = UserListSerializer(user, many=True)

            response_data = {"users": out_serializer.data}

            return Response(data=response_data)

        except NotFound as e:
            raise NotFound({"message": str(e), "extra": {}}, status=404)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "extra": {"details": str(e)}}, status=500)


class UserDetailAPI(ApiAuthMixin, APIView):
    serializer_class = UserDetailSerializer

    def get(self, request, user_id):
        try:
            user_instance = get_object_or_404(User, id=user_id)

            output_serializer = UserDetailSerializer(user_instance)

            response_data = {"user": output_serializer.data}

            return Response(data=response_data)

        except NotFound as e:
            raise NotFound(e)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "extra": {"details": str(e)}}, status=500)
