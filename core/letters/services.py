from collections import OrderedDict
from typing import Optional, Union

from django.db import transaction

from core.attachments.services import attachment_create
from core.participants.services import participants_create
from core.participants.utils import identify_participants_changes
from core.users.models import Member
from core.workflows.services import letter_publish

from .models import Incoming, Internal, Letter, Outgoing

type LetterParticipant = dict[str, Union[str, int, dict[str, str], list[str]]]


# Create a letter instance based on the provided letter_type and keyword arguments.
def create_letter_instance(letter_type: str, current_user: Member, **kwargs) -> Letter:
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
    current_user: Member,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    signature=None,
    letter_type: str,
    participants,
    attachments=None,
) -> Letter:
    letter_data = {
        "letter_type": letter_type,
        "current_user": current_user,
        "subject": subject,
        "content": content,
        "current_state": Letter.States.DRAFT,
        "owner": current_user,
    }

    if signature is not None:
        letter_data["signature"] = signature

    letter_instance = create_letter_instance(**letter_data)

    if letter_type in ["internal", "outgoing"]:
        author_participant = OrderedDict({
            "id": "",
            "user": OrderedDict({
                "id": current_user.id,
                "user_type": "member",
            }),
            "role": "Author",
        })
        participants.append(author_participant)

    participants_create(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=participants,
    )
    if attachments is not None:
        attachment_create(
            current_user=current_user,
            letter_instance=letter_instance,
            attachments=attachments,
        )

    return letter_instance


@transaction.atomic
def letter_create_and_publish(
    *,
    current_user: Member,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    signature=None,
    letter_type: str,
    participants,
    attachments=None,
) -> Letter:
    letter_data = {
        "letter_type": letter_type,
        "current_user": current_user,
        "subject": subject,
        "content": content,
        "current_state": Letter.States.DRAFT,
        "owner": current_user,
    }

    if signature is not None:
        letter_data["signature"] = signature

    letter_instance = create_letter_instance(**letter_data)

    letter_instance.current_state = Letter.States.SUBMITTED
    letter_instance.save()

    participants_create(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=participants,
    )
    if attachments is not None:
        attachment_create(
            current_user=current_user,
            letter_instance=letter_instance,
            attachments=attachments,
        )

    letter_publish(current_user=current_user, letter_instance=letter_instance)

    return letter_instance


@transaction.atomic
def letter_update(
    current_user: Member,
    letter_instance: Letter,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    letter_type: str = "internal",
    signature=None,
    attachments=None,
    participants: Optional[list[LetterParticipant]] = None,
) -> Letter:
    if subject is not None:
        letter_instance.subject = subject

    if content is not None:
        letter_instance.content = content

    if signature is not None:
        letter_instance.signature = signature

    letter_instance.save()

    participants_to_add, participants_to_remove = identify_participants_changes(
        letter_instance=letter_instance,
        new_participants=participants,
    )

    participants_to_remove.delete()

    participants_create(
        current_user=current_user,
        participants=participants_to_add,
        letter_instance=letter_instance,
    )

    if attachments is not None:
        attachment_create(
            current_user=current_user,
            letter_instance=letter_instance,
            attachments=attachments,
        )

    return letter_instance
