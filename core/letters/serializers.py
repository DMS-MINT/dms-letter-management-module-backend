from rest_framework import serializers

from core.common.utils import inline_serializer
from core.participants.models import Participant
from core.users.apis import UserListApi
from core.users.serializers import MemberListSerializer, UserCreateSerializer


class LetterListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    reference_number = serializers.SlugField()
    owner = MemberListSerializer()
    current_state = serializers.CharField(source="get_current_state_display")
    subject = serializers.CharField()
    participants = inline_serializer(
        many=True,
        fields={
            "id": serializers.UUIDField(),
            "user": UserListApi.OutputSerializer(),
            "role": serializers.ChoiceField(choices=Participant.Roles.choices, source="get_role_display"),
        },
    )
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
    current_state = serializers.CharField(source="get_current_state_display")
    subject = serializers.CharField()
    content = serializers.CharField()
    owner = MemberListSerializer()
    language = serializers.CharField(source="get_language_display")
    pdf_version = serializers.URLField()
    participants = inline_serializer(
        many=True,
        fields={
            "id": serializers.UUIDField(),
            "user": UserListApi.OutputSerializer(),
            "role": serializers.ChoiceField(choices=Participant.Roles.choices, source="get_role_display"),
        },
    )
    comments = inline_serializer(
        many=True,
        fields={
            "id": serializers.UUIDField(),
            "content": serializers.CharField(),
            "author": MemberListSerializer(),
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


class LetterCreateSerializer(serializers.Serializer):
    subject = serializers.CharField(required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True)
    letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])
    language = serializers.ChoiceField(choices=["EN", "AM"])
    participants = inline_serializer(
        many=True,
        fields={
            "id": serializers.UUIDField(required=False),
            "user": UserCreateSerializer(),
            "role": serializers.CharField(),
        },
    )
