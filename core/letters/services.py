from django.db import transaction

from .models import Incoming, Internal, Letter, Outgoing


@transaction.atomic
def letter_create(*, validated_data):
    letter_type = validated_data.get("letter_type")

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

    return instance
