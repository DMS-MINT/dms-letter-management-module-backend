from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object, inline_serializer
from core.permissions.service import check_permissions
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
GET_LETTER_HRF = "api/letters/<uuid:letter_id>/"
CREATE_LETTER_HRF = "api/letters/create/"
UPDATE_LETTER_HRF = "api/letters/<uuid:letter_id>/update/"
DELETE_LETTER_HRF = "api/letters/<uuid:letter_id>/delete/"
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
        category = serializers.ChoiceField(choices=["inbox", "outbox", "draft"], required=True)

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
        filter_serializer.is_valid(raise_exception=False)

        letter_instances = letter_list(user=request.user, filters=filter_serializer.validated_data)

        serializer = self.OutputSerializer(letter_instances, many=True)

        response_data = {"action": ACTIONS, "data": serializer.data}

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "letter_type"
        model_serializer_mapping = {
            Internal: LetterDetailSerializer,
            Incoming: LetterDetailSerializer,
            Outgoing: OutgoingLetterDetailSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    def get(self, request, letter_id) -> Response:
        letter = get_object(Letter, id=letter_id)

        serializer = self.OutputSerializer(letter, many=False)

        response_data = {"action": ACTIONS, "data": serializer.data}

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False)
        content = serializers.CharField(required=False)
        letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])
        participants = inline_serializer(
            many=True,
            fields={"user": UserCreateSerializer(), "role_name": serializers.CharField()},
        )

    def post(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_create(user=request.user, **input_serializer.validated_data)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

            response_data = {"action": ACTIONS, "data": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False, allow_blank=True)
        content = serializers.CharField(required=False, allow_blank=True)
        participants = inline_serializer(
            many=True,
            required=False,
            fields={"user": UserCreateSerializer(), "role_name": serializers.CharField()},
        )

    def put(self, request, letter_id) -> Response:
        letter_instance = get_object_or_404(Letter, pk=letter_id)
        check_permissions(letter_instance=letter_instance, user=request.user, actions=["edit"])

        input_serializer = self.InputSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_update(
                user=request.user,
                letter_instance=letter_instance,
                **input_serializer.validated_data,
            )
            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

            response_data = {"action": ACTIONS, "data": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, letter_id) -> Response:
        letter_instance = get_object_or_404(Letter, pk=letter_id)
        check_permissions(letter_instance=letter_instance, user=request.user, actions=["delete"])

        letter_instance.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)
