from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.participants.apis import ParticipantListApi

from ..common.utils import get_list, get_object
from .models import Incoming, Internal, Letter, Outgoing


class LetterListSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.ChoiceField(choices=Letter.LetterStatus.choices, source="get_status_display")

    class Meta:
        model = Letter
        fields: list[str] = [
            "id",
            "status",
            "subject",
            "created",
            "modified",
        ]


class LetterListApi(APIView):
    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "user_type"
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


class LetterDetailSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.ChoiceField(choices=Letter.LetterStatus.choices, source="get_status_display")
    letter_participants = ParticipantListApi.OutputSerializer(many=True)

    class Meta:
        model = Letter
        fields: list[str] = [
            "id",
            "status",
            "subject",
            "content",
            "letter_participants",
            "created",
            "modified",
        ]


class OutgoingLetterDetailSerializer(LetterDetailSerializer):
    class Meta(LetterDetailSerializer.Meta):
        model = Outgoing
        fields: list[str] = LetterDetailSerializer.Meta.fields + [
            "delivery_person_name",
            "delivery_person_phone",
            "shipment_id",
        ]


class LetterDetailApi(APIView):
    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "user_type"
        model_serializer_mapping = {
            Internal: LetterDetailSerializer,
            Incoming: LetterDetailSerializer,
            Outgoing: OutgoingLetterDetailSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    def get(self, request, letter_id) -> Response:
        letter = get_object(Letter, id=letter_id)

        if letter is None:
            return Response({"detail": "Letter not found"}, status=404)

        serializer = self.OutputSerializer(letter, many=False)
        return Response(data=serializer.data)
