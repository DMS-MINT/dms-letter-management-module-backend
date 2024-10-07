from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin, HasTenantAccess
from core.common.utils import get_object
from core.user_management.selectors import user_profile_details
from core.users.models import User

from .selectors import user_get_users
from .serializers import UserDetailSerializer, UserListSerializer
from .services import user_create, user_update


class UserListApi(APIView):
    permission_classes = [IsAuthenticated]

    class FilterSerializer(serializers.Serializer):
        filter = serializers.ChoiceField(
            choices=[
                ("all", "All users"),
                ("staff", "Staff only"),
                ("superuser", "Superusers only"),
                ("staff_and_superuser", "Staff and Superusers"),
            ],
            required=True,
        )

    serializer_class = UserListSerializer
    filter_class = FilterSerializer

    def get(self, request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        try:
            users = user_get_users(current_user=request.user, filters=filter_serializer.validated_data)

            users_list = []
            for user_instance in users:
                user_profile_instance = user_profile_details(user_instance=user_instance)
                users_list.append(user_profile_instance)

            # output_serializer = UserDetailSerializer(user_profile_instance)

            output_serializer = UserDetailSerializer(users_list, many=True)

            response_data = {"users": output_serializer.data}

            return Response(data=response_data)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated, HasTenantAccess]
    serializer_class = UserDetailSerializer

    def get(self, request, user_id):
        try:
            user_instance = User.objects.prefetch_related("user_profile").get(id=user_id)

            user_profile_instance = user_profile_details(user_instance=user_instance)

            output_serializer = UserDetailSerializer(user_profile_instance)

            response_data = {"user": output_serializer.data}

            return Response(data=response_data)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserCreateApi(APIView):
    permission_classes = [IsAuthenticated]

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

            user_profile = user_profile_details(user_instance=user_instance)

            output_serializer = UserListSerializer(user_profile)

            response_data = {"user": output_serializer.data}

            return Response(data=response_data)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserUpdateApi(APIView):
    permission_classes = [IsAuthenticated, HasTenantAccess]

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
        input_serializer = self.serializer_class(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            user_instance = User.objects.prefetch_related("user_profile").get(id=user_id)

            user_instance = user_update(user_instance=user_instance, **input_serializer.validated_data)

            user_profile = user_profile_details(user_instance=user_instance)

            output_serializer = UserListSerializer(user_profile)

            response_data = {"user": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except User.DoesNotExist as e:
            raise NotFound(e)

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
