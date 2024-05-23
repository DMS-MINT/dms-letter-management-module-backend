from rest_framework import serializers

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
