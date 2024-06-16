from typing import Optional, Union

from django.db import transaction

from core.participants.models import Participant
from core.participants.services import participant_create
from core.users.models import Member

from .models import Incoming, Internal, Letter, Outgoing, State

type LetterParticipant = dict[str, Union[str, int, dict[str, str]]]


# Create a letter instance based on the provided letter_type and keyword arguments.
def create_letter_instance(letter_type: str, current_user: Member, **kwargs) -> Letter:
    letter_instance_class = {
        "internal": Internal,
        "incoming": Incoming,
        "outgoing": Outgoing,
    }.get(letter_type)

    if letter_instance_class:
        letter_instance = letter_instance_class(**kwargs)
        letter_instance.save(current_user=current_user)
        return letter_instance

    raise ValueError("Invalid letter type")


def get_enum_value(key):
    for role in Participant.RoleNames:
        if role.label.lower() == key.lower():
            return role.value
    raise ValueError(f"No matching participant role value for key: {key}")


# This function orchestrates the creation of a letter and its participants in a transaction.
@transaction.atomic
def letter_create(
    *,
    current_user: Member,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    letter_type: str,
    participants: list[LetterParticipant],
) -> Letter:
    letter_instance = create_letter_instance(
        letter_type=letter_type,
        current_user=current_user,
        subject=subject,
        content=content,
        current_state=State.objects.get(name="Draft"),
    )

    participant_create(participants=participants, letter=letter_instance)

    return letter_instance


@transaction.atomic
def letter_update(
    current_user: Member,
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
        existing_participants = set(letter_instance.participants.values_list("id", flat=True))
        new_participants = set(participant["id"] for participant in participants)

        participants_to_remove_ids = existing_participants - new_participants
        participants_to_add_ids = new_participants - existing_participants

        participants_to_add = [
            participant for participant in participants if participant["id"] in participants_to_add_ids
        ]

        letter_instance.participants.filter(id__in=participants_to_remove_ids).delete()
        participant_create(current_user=current_user, participants=participants_to_add, letter_instance=letter_instance)

    return letter_instance
