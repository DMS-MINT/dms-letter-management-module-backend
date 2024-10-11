from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin

from .selectors import member_list, member_profile_details
from .serializers import MemberDetailSerializer, MemberListSerializer
from .services import user_create


class MemberListApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        filter = serializers.ChoiceField(
            choices=[
                ("all", "All users"),
                ("staff", "Staff only"),
                ("admin", "Admin only"),
                ("staff_and_admin", "Staff and Admin"),
            ],
            required=True,
        )
        include_current_user = serializers.BooleanField(required=False, default=False)

    serializer_class = MemberListSerializer
    filter_class = FilterSerializer

    def get(self, request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        try:
            members = member_list(current_user=request.user, filters=filter_serializer.validated_data)

            output_serializer = self.serializer_class(members, many=True)

            response_data = {"members": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class MemberCreateApi(ApiAuthMixin, APIView):
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

        is_admin = serializers.BooleanField()
        is_staff = serializers.BooleanField()

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            user_create(**input_serializer.validated_data)

            response_data = {"message": "User has been successfully added to the tenant."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class MemberDetailApi(ApiAuthMixin, APIView):
    serializer_class = MemberDetailSerializer

    def get(self, request, member_id) -> Response:
        try:
            member_instance = member_profile_details(member_id=member_id)

            output_serializer = MemberDetailSerializer(member_instance)

            response_data = {"member": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
