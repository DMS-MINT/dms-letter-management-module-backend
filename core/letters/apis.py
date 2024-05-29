from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.common.utils import get_object, inline_serializer
from core.participants.models import Participant
from core.users.serializers import UserCreateSerializer

from .models import Incoming, Internal, Letter, Outgoing
from .selectors import letter_list
from .serializers import (
    LetterDetailSerializer,
    LetterListSerializer,
    OutgoingLetterDetailSerializer,
)
from .services import letter_create, letter_update


class LetterListApi(APIView):
    class FilterSerializer(serializers.Serializer):
        category = serializers.ChoiceField(choices=["inbox", "outbox", "draft"], required=True)
        # status = serializers.ChoiceField(choices=Letter.LetterStatus.choices)

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

        letters = letter_list(filters=filter_serializer.validated_data)

        serializer = self.OutputSerializer(letters, many=True)

        response_data = {
            "action": [
                {
                    "name": "Letter Details",
                    "hrf": "",
                    "method": "GET",
                },
                {
                    "name": "Update Letter",
                    "hrf": "",
                    "method": "PUT",
                },
                {
                    "name": "Delete Letter",
                    "hrf": "",
                    "method": "DELETE",
                },
            ],
            "data": serializer.data,
        }

        return Response(data=response_data)


class LetterDetailApi(APIView):
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

        response_data = {
            "action": [
                {
                    "name": "Letter Listing",
                    "hrf": "",
                    "method": "GET",
                },
                {
                    "name": "Update Letter",
                    "hrf": "",
                    "method": "PUT",
                },
                {
                    "name": "Delete Letter",
                    "hrf": "",
                    "method": "DELETE",
                },
            ],
            "data": serializer.data,
        }

        return Response(data=response_data)


class LetterCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False)
        content = serializers.CharField(required=False)
        status = serializers.ChoiceField(choices=Letter.LetterStatus.choices)
        letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])
        participants = inline_serializer(
            many=True,
            fields={
                "user": UserCreateSerializer(),
                "role": serializers.ChoiceField(choices=Participant.Roles.choices),
                "message": serializers.CharField(required=False, allow_null=True),
            },
        )

    def post(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_create(**input_serializer.validated_data)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

            response_data = {
                "action": [
                    {
                        "name": "Update Letter",
                        "hrf": "",
                        "method": "PUT",
                    },
                    {
                        "name": "Delete Letter",
                        "hrf": "",
                        "method": "DELETE",
                    },
                ],
                "data": output_serializer.data,
            }

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False, allow_blank=True)
        content = serializers.CharField(required=False, allow_blank=True)
        participants = inline_serializer(
            many=True,
            required=False,
            fields={
                "user": UserCreateSerializer(),
                "role": serializers.ChoiceField(choices=Participant.Roles.choices),
                "message": serializers.CharField(required=False, allow_null=True, allow_blank=True),
            },
        )

    def put(self, request, letter_id) -> Response:
        letter_instance = get_object_or_404(Letter, pk=letter_id)
        input_serializer = self.InputSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_update(letter_instance, **input_serializer.validated_data)
            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

            response_data = {
                "action": [
                    {
                        "name": "Update Letter",
                        "hrf": "",
                        "method": "PUT",
                    },
                    {
                        "name": "Delete Letter",
                        "hrf": "",
                        "method": "DELETE",
                    },
                ],
                "data": output_serializer.data,
            }

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class DeleteLetterApi(APIView):
    def delete(self, request, letter_id) -> Response:
        letter_instance = get_object_or_404(Letter, pk=letter_id)
        letter_instance.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)
