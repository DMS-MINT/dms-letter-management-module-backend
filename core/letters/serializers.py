from rest_framework import serializers

from core.common.utils import inline_serializer
from core.participants.models import Participant
from core.users.apis import UserListApi
from core.users.serializers import MemberListSerializer


class LetterListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    reference_number = serializers.SlugField()
    owner = MemberListSerializer()
    current_state = inline_serializer(many=False, fields={"name": serializers.CharField()})
    subject = serializers.CharField()
    participants = inline_serializer(
        many=True,
        fields={
            "role": serializers.ChoiceField(choices=Participant.RoleNames.choices, source="get_role_display"),
            "user": UserListApi.OutputSerializer(),
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
    reference_number = serializers.SlugField()
    owner = MemberListSerializer()
    current_state = inline_serializer(many=False, fields={"name": serializers.CharField()})
    subject = serializers.CharField()
    content = serializers.CharField()
    participants = inline_serializer(
        many=True,
        fields={
            "id": serializers.UUIDField(),
            "user": UserListApi.OutputSerializer(),
            "role": serializers.ChoiceField(choices=Participant.RoleNames.choices, source="get_role_display"),
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
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class OutgoingLetterDetailSerializer(LetterDetailSerializer):
    delivery_person_name = serializers.CharField()
    delivery_person_phone = serializers.DateTimeField()
    shipment_id = serializers.DateTimeField()
