from rest_framework import serializers

from core.common.utils import inline_serializer
from core.participants.models import Participant
from core.users.apis import UserListApi

from .models import Letter


class LetterListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=Letter.LetterStatus.choices, source="get_status_display")
    subject = serializers.CharField()
    participants = inline_serializer(
        many=True,
        fields={
            "user": UserListApi.OutputSerializer(),
            "role": serializers.ChoiceField(choices=Participant.Roles.choices, source="get_role_display"),
        },
    )
    has_read: serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret["has_read"] = True

        return ret


class LetterDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=Letter.LetterStatus.choices, source="get_status_display")
    subject = serializers.CharField()
    content = serializers.CharField()
    participants = inline_serializer(
        many=True,
        fields={
            "user": UserListApi.OutputSerializer(),
            "role": serializers.ChoiceField(choices=Participant.Roles.choices, source="get_role_display"),
            "message": serializers.CharField(),
        },
    )
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class OutgoingLetterDetailSerializer(LetterDetailSerializer):
    delivery_person_name = serializers.CharField()
    delivery_person_phone = serializers.DateTimeField()
    shipment_id = serializers.DateTimeField()
