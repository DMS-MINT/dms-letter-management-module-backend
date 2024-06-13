from collections import OrderedDict
from typing import Optional, Union

from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from core.participants.models import Participant, Role
from core.participants.services import participant_create
from core.users.models import Member

from .models import Incoming, Internal, Letter, Outgoing, State

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


def check_permission(letter_instance, user, action):
    try:
        letter_participants = letter_instance.participants.filter(user=user)
    except Participant.DoesNotExist:
        raise PermissionDenied("You are not a participant in this letter.")

    if not letter_instance.state.can_be(action):
        raise PermissionDenied(f"The letter cannot be {action} in its current state.")

    can_take_action = any(participant.role.can(action) for participant in letter_participants)
    if not can_take_action:
        raise PermissionDenied(f"You do not have permission to {action} this letter.")

    return True


# This function orchestrates the creation of a letter and its participants in a transaction.
@transaction.atomic
def letter_create(
    *,
    user: Member,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    letter_type: str,
    participants: list[LetterParticipant],
) -> Letter:
    letter_instance = create_letter_instance(
        letter_type,
        subject=subject,
        content=content,
        state=State.objects.get(name="Draft"),
    )

    editor_participant = OrderedDict({
        "user": OrderedDict({
            "id": user.id,
            "user_type": "member",
        }),
        "role": Role.objects.get(name="Editor"),
    })

    participants.append(editor_participant)
    participant_create(participants=participants, letter=letter_instance)

    return letter_instance


@transaction.atomic
def letter_update(
    user: Member,
    letter_instance: Letter,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    participants: Optional[list[LetterParticipant]] = None,
) -> Letter:
    check_permission(letter_instance, user, "edit")

    if subject is not None:
        letter_instance.subject = subject

    if content is not None:
        letter_instance.content = content

    letter_instance.save()

    if participants is not None:
        letter_instance.participants.all().delete()
        participant_create(participants=participants, letter=letter_instance)

    return letter_instance


@transaction.atomic
def submit_letter_for_review(user: Member, letter_instance: Letter, to: str, message: str) -> Letter:
    check_permission(letter_instance, user, "submit_for_review")

    reviewer = [
        {
            "user": OrderedDict({
                "id": to,
                "user_type": "member",
            }),
            "role": Role.objects.get(name="Reviewer"),
        },
    ]

    participant_create(participants=reviewer, letter=letter_instance)

    return letter_instance


@transaction.atomic
def submit_letter_for_publishing(user: Member, letter_instance: Letter) -> Letter:
    check_permission(letter_instance, user, "submit_for_publishing")

    letter_instance.state = State.objects.get("Submitted")

    return letter_instance


@transaction.atomic
def retract_letter(user: Member, letter_instance: Letter) -> Letter:
    check_permission(letter_instance, user, "retract")

    letter_instance.state = State.objects.get("Retracted")

    return letter_instance


@transaction.atomic
def publish_letter(user: Member, letter_instance: Letter, publisher: str) -> Letter:
    check_permission(letter_instance, user, "submit_for_review")

    letter_instance.state = State.objects.get("	Published")

    administrator = [
        {
            "user": OrderedDict({
                "id": publisher,
                "user_type": "member",
            }),
            "role": Role.objects.get(name="Administrator"),
        },
    ]

    participant_create(participants=administrator, letter=letter_instance)

    return letter_instance


@transaction.atomic
def forward_letter(user: Member, letter_instance: Letter, to: str, message: str) -> Letter:
    check_permission(letter_instance, user, "forward")

    forward_recipient = [
        {
            "user": OrderedDict({
                "id": to,
                "user_type": "member",
            }),
            "role": Role.objects.get(name="Forward Recipient"),
        },
    ]

    participant_create(participants=forward_recipient, letter=letter_instance)

    return letter_instance
