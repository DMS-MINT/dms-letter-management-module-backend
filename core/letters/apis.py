from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.common.utils import get_list, get_object, inline_serializer
from core.participants.models import Participant
from core.users.serializers import UserCreateSerializer

from .models import Incoming, Internal, Letter, Outgoing
from .serializers import (
    LetterDetailSerializer,
    LetterListSerializer,
    OutgoingLetterDetailSerializer,
)
from .services import letter_create


class LetterListApi(APIView):
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
        letters = get_list(Letter)

        serializer = self.OutputSerializer(letters, many=True)

        return Response(data=serializer.data)


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

        return Response(data=serializer.data)


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
                        "hrf": "http://127.0.0.1:8000/api/letters/update/",
                        "method": "PUT",
                    },
                    {
                        "name": "Delete Letter",
                        "hrf": "http://127.0.0.1:8000/api/letters/delete/",
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
