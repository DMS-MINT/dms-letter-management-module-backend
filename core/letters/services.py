from django.core.exceptions import ValidationError
from django.db import transaction

from core.participants.services import participant_create

from .models import Incoming, Internal, Outgoing


@transaction.atomic
def letter_create(*, validated_data):
    letter_type = validated_data.get("letter_type")
    participants_data = validated_data.get("participants")

    try:
        if letter_type == "internal":
            instance = Internal.objects.create(
                subject=validated_data.get("subject"),
                content=validated_data.get("content"),
                status=validated_data.get("status"),
            )
        elif letter_type == "incoming":
            instance = Incoming.objects.create(
                subject=validated_data.get("subject"),
                content=validated_data.get("content"),
                status=validated_data.get("status"),
            )
        elif letter_type == "outgoing":
            instance = Outgoing.objects.create(
                subject=validated_data.get("subject"),
                content=validated_data.get("content"),
                status=validated_data.get("status"),
            )
        else:
            raise ValueError("Invalid letter_type provided")

        participant_create(validated_data=participants_data, letter_id=instance.id)

    except ValidationError as e:
        raise ValueError(f"Unable to create letter: {e}")

    return instance
