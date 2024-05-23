from rest_framework import serializers

from core.common.utils import inline_serializer
from core.participants.models import Participant
from core.users.apis import UserListApi

from .models import Letter


class LetterListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=Letter.LetterStatus.choices, source="get_status_display")
    subject = serializers.CharField()
    created = serializers.DateTimeField()
    modified = serializers.DateTimeField()


class LetterDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=Letter.LetterStatus.choices, source="get_status_display")
    subject = serializers.CharField()
    content = serializers.CharField()
    letter_participants = inline_serializer(
        many=True,
        fields={
            "user": UserListApi.OutputSerializer(),
            "role": serializers.ChoiceField(choices=Participant.Roles.choices, source="get_role_display"),
            "message": serializers.CharField(),
        },
    )
    created = serializers.DateTimeField()
    modified = serializers.DateTimeField()


class OutgoingLetterDetailSerializer(LetterDetailSerializer):
    delivery_person_name = serializers.CharField()
    delivery_person_phone = serializers.DateTimeField()
    shipment_id = serializers.DateTimeField()


class LetterCreateSerializer(serializers.Serializer):
    subject = serializers.CharField()
    content = serializers.CharField()
    status = serializers.ChoiceField(choices=Letter.LetterStatus.choices)
