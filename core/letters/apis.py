from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object, inline_serializer
from core.permissions.mixins import ApiPermMixin
from core.users.serializers import UserCreateSerializer

from .models import Incoming, Internal, Letter, Outgoing
from .selectors import letter_list
from .serializers import (
    LetterDetailSerializer,
    LetterListSerializer,
    OutgoingLetterDetailSerializer,
)
from .services import letter_create, letter_update

GET_LETTERS_HRF = "api/letter/"
GET_LETTER_HRF = "api/letters/<slug:reference_number>/"
CREATE_LETTER_HRF = "api/letters/create/"
UPDATE_LETTER_HRF = "api/letters/<slug:reference_number>/update/"
DELETE_LETTER_HRF = "api/letters/<slug:reference_number>/delete/"
ACTIONS = (
    [
        {
            "name": "Letter Listing",
            "hrf": GET_LETTERS_HRF,
            "method": "GET",
        },
        {
            "name": "Letter Details",
            "hrf": GET_LETTER_HRF,
            "method": "GET",
        },
        {
            "name": "Create Letter",
            "hrf": CREATE_LETTER_HRF,
            "method": "PUT",
        },
        {
            "name": "Update Letter",
            "hrf": UPDATE_LETTER_HRF,
            "method": "PUT",
        },
        {
            "name": "Delete Letter",
            "hrf": DELETE_LETTER_HRF,
            "method": "DELETE",
        },
    ],
)


class LetterListApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        category = serializers.ChoiceField(
            choices=["inbox", "outbox", "draft", "pending", "published"],
            required=True,
        )

    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "letter_type"
        model_serializer_mapping = {
            Internal: LetterListSerializer,
            Incoming: LetterListSerializer,
            Outgoing: LetterListSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    def get(self, request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        letter_instances = letter_list(current_user=request.user, filters=filter_serializer.validated_data)

        serializer = self.OutputSerializer(letter_instances, many=True)

        response_data = {"action": ACTIONS, "data": serializer.data}

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterDetailApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter"]

    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "letter_type"
        model_serializer_mapping = {
            Internal: LetterDetailSerializer,
            Incoming: LetterDetailSerializer,
            Outgoing: OutgoingLetterDetailSerializer,
        }

        def to_resource_type(self, instance):
            return instance._meta.object_name.lower()

    def get(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)
        if request.user.is_staff:
            assign_perm("can_view_letter", request.user, letter_instance)
            assign_perm("can_publish_letter", request.user, letter_instance)

        self.check_object_permissions(request, letter_instance)

        output_serializer = self.OutputSerializer(letter_instance, many=False)
        permissions = self.get_object_permissions(request, letter_instance)

        response_data = {
            "action": ACTIONS,
            "data": output_serializer.data,
            "permissions": permissions,
        }

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterCreateApi(ApiAuthMixin, ApiPermMixin, APIView):
    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False)
        content = serializers.CharField(required=False)
        letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])
        participants = inline_serializer(
            many=True,
            fields={
                "user": UserCreateSerializer(),
                "role": serializers.CharField(),
                "permissions": serializers.ListField(
                    required=False,
                    child=serializers.ChoiceField(
                        choices=[
                            "can_view_letter",
                            "can_update_letter",
                            "can_comment_letter",
                            "can_share_letter",
                        ],
                    ),
                ),
            },
        )

    def post(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_create(current_user=request.user, **input_serializer.validated_data)
            permissions = self.get_object_permissions(request, letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

            response_data = {
                "action": ACTIONS,
                "data": output_serializer.data,
                "permissions": permissions,
            }

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterUpdateApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_update_letter"]

    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False, allow_blank=True)
        content = serializers.CharField(required=False, allow_blank=True)
        participants = inline_serializer(
            many=True,
            required=False,
            fields={
                "id": serializers.UUIDField(),
                "user": UserCreateSerializer(),
                "role": serializers.CharField(),
            },
        )

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        input_serializer = self.InputSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_update(
                current_user=request.user,
                letter_instance=letter_instance,
                **input_serializer.validated_data,
            )
            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions(request, letter_instance)

            response_data = {
                "action": ACTIONS,
                "data": output_serializer.data,
                "permissions": permissions,
            }

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterDeleteApi(ApiAuthMixin, APIView):
    required_object_perms = ["can_view_letter", "can_delete_letter"]

    def delete(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        letter_instance.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)
