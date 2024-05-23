from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.participants.apis import ParticipantCreateApi

from ..common.utils import get_list, get_object
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
        subject = serializers.CharField()
        content = serializers.CharField()
        status = serializers.ChoiceField(choices=Letter.LetterStatus.choices)
        participants = serializers.ListField(child=ParticipantCreateApi.InputSerializer())
        letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])

    def post(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)

        if input_serializer.is_valid():
            try:
                letter_instance = letter_create(validated_data=input_serializer.validated_data)

                output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

                return Response(data=output_serializer.data, status=http_status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({"detail": str(e)}, status=http_status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({"detail": str(e)}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(input_serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
