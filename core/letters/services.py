from typing import Optional, Union

from django.db import transaction

from core.participants.services import participant_create

from .models import Incoming, Internal, Letter, Outgoing

type LetterParticipant = dict[str, Union[str, int, dict[str, str]]]


# Create a letter instance based on the provided letter_type and keyword arguments.
def create_letter_instance(letter_type: str, **kwargs) -> Letter:
    letter_instance_class = {
        "internal": Internal,
        "incoming": Incoming,
        "outgoing": Outgoing,
    }.get(letter_type)

    if letter_instance_class:
        return letter_instance_class.objects.create(**kwargs)

    raise ValueError("Invalid letter type")


# This function orchestrates the creation of a letter and its participants in a transaction.
@transaction.atomic
def letter_create(
    *,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    status: int,
    letter_type: str,
    participants: list[LetterParticipant],
) -> Letter:
    letter_instance = create_letter_instance(letter_type, subject=subject, content=content, status=status)

    participant_create(participants=participants, letter=letter_instance)

    return letter_instance


@transaction.atomic
def letter_update(
    letter_instance: Letter,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    participants: Optional[list[LetterParticipant]] = None,
) -> Letter:
    if subject is not None:
        letter_instance.subject = subject
    if content is not None:
        letter_instance.content = content

    letter_instance.save()

    if participants is not None:
        letter_instance.participants.all().delete()
        participant_create(participants=participants, letter=letter_instance)

    return letter_instance
