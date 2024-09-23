from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from core.common.utils import inline_serializer
from core.participants.serializers import ParticipantInputSerializer, ParticipantOutputSerializer
from core.users.serializers import UserListSerializer

from .models import Incoming, Internal, Outgoing


class LetterListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    reference_number = serializers.SlugField()
    reference_number_am = serializers.SlugField()
    owner = UserListSerializer()
    current_state = serializers.CharField(source="get_current_state_display")
    subject = serializers.CharField()
    participants = ParticipantOutputSerializer(many=True)
    has_read: serializers.SerializerMethodField()
    submitted_at = serializers.DateTimeField()
    published_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret["has_read"] = True

        return ret


class LetterDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    reference_number = serializers.SlugField()
    reference_number_am = serializers.SlugField()
    current_state = serializers.CharField(source="get_current_state_display")
    subject = serializers.CharField()
    body = serializers.CharField()
    owner = UserListSerializer()
    language = serializers.CharField(source="get_language_display")
    pdf_version = serializers.URLField()
    participants = ParticipantOutputSerializer(many=True)
    comments = inline_serializer(
        many=True,
        fields={
            "id": serializers.UUIDField(),
            "message": serializers.CharField(),
            "author": UserListSerializer(),
            "created_at": serializers.DateTimeField(),
        },
    )
    letter_attachments = inline_serializer(
        many=True,
        fields={
            "id": serializers.UUIDField(),
            "file": serializers.CharField(),
            "file_name": serializers.CharField(),
            "file_type": serializers.CharField(),
            "file_size": serializers.CharField(),
            "uploaded_by": UserListSerializer(),
            "description": serializers.CharField(),
            "created_at": serializers.DateTimeField(),
        },
    )
    submitted_at = serializers.DateTimeField()
    published_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class OutgoingLetterDetailSerializer(LetterDetailSerializer):
    delivery_person_name = serializers.CharField()
    delivery_person_phone = serializers.DateTimeField()
    shipment_id = serializers.DateTimeField()


class LetterDetailPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "letter_type"
    model_serializer_mapping = {
        Internal: LetterDetailSerializer,
        Incoming: LetterDetailSerializer,
        Outgoing: OutgoingLetterDetailSerializer,
    }

    def to_resource_type(self, instance):
        return instance._meta.object_name.lower()


class LetterCreateSerializer(serializers.Serializer):
    subject = serializers.CharField(required=False, allow_blank=True)
    body = serializers.CharField(required=False, allow_blank=True)
    letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])
    language = serializers.ChoiceField(choices=["EN", "AM"])
    participants = ParticipantInputSerializer(many=True)
