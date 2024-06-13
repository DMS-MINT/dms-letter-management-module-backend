from rest_framework import serializers

from core.common.utils import inline_serializer
from core.users.apis import UserListApi


class RoleSerializer(serializers.Serializer):
    name = serializers.CharField()
    permissions = serializers.JSONField()


class StateSerializer(serializers.Serializer):
    name = serializers.CharField()
    permissions = serializers.JSONField()


class LetterListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    state = StateSerializer
    subject = serializers.CharField()
    participants = inline_serializer(
        many=True,
        fields={
            "user": UserListApi.OutputSerializer(),
            "role": RoleSerializer,
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
    state = StateSerializer
    subject = serializers.CharField()
    content = serializers.CharField()
    participants = inline_serializer(
        many=True,
        fields={
            "user": UserListApi.OutputSerializer(),
            "role": RoleSerializer,
        },
    )
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class OutgoingLetterDetailSerializer(LetterDetailSerializer):
    delivery_person_name = serializers.CharField()
    delivery_person_phone = serializers.DateTimeField()
    shipment_id = serializers.DateTimeField()
