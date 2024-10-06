from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object
from core.users.models import User

from .selectors import user_get_users
from .serializers import UserDetailSerializer, UserListSerializer
from .services import user_create, user_update


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

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserDetailAPI(ApiAuthMixin, APIView):
    serializer_class = UserDetailSerializer

    def get(self, request, user_id):
        try:
            user_instance = get_object_or_404(User, id=user_id)

            output_serializer = UserDetailSerializer(user_instance)

            response_data = {"user": output_serializer.data}

            return Response(data=response_data)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

        first_name_en = serializers.CharField()
        middle_name_en = serializers.CharField()
        last_name_en = serializers.CharField()

        first_name_am = serializers.CharField()
        middle_name_am = serializers.CharField()
        last_name_am = serializers.CharField()

        job_title = serializers.UUIDField()
        department = serializers.UUIDField()
        phone_number = serializers.IntegerField()

        is_staff = serializers.BooleanField()
        is_superuser = serializers.BooleanField()

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            user_instance = user_create(**input_serializer.validated_data)

            output_serializer = UserListSerializer(user_instance)

            response_data = {"user": output_serializer.data}

            return Response(data=response_data)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)

        first_name_en = serializers.CharField(required=False)
        middle_name_en = serializers.CharField(required=False)
        last_name_en = serializers.CharField(required=False)

        first_name_am = serializers.CharField(required=False)
        middle_name_am = serializers.CharField(required=False)
        last_name_am = serializers.CharField(required=False)

        job_title = serializers.UUIDField(required=False)
        department = serializers.UUIDField(required=False)
        phone_number = serializers.IntegerField(required=False)

        is_staff = serializers.BooleanField(required=False)
        is_superuser = serializers.BooleanField(required=False)

    serializer_class = InputSerializer

    def put(self, request, user_id):
        user_instance = get_object(User, id=user_id)
        input_serializer = self.serializer_class(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            user_instance = user_update(user_instance=user_instance, **input_serializer.validated_data)

            output_serializer = UserDetailSerializer(user_instance)

            response_data = {"user": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, user_id):
        user_instance = get_object(User, id=user_id)

        try:
            user_instance.delete()

            response_data = {"message": "User removed from your organization successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
