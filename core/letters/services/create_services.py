from collections import OrderedDict
from typing import Optional, Union

from django.db import transaction

from core.attachments.services import letter_attachment_create
from core.letters.models import Incoming, Internal, Letter, Outgoing
from core.participants.services import participants_create
from core.users.models import User
from core.workflows.services import letter_publish

type LetterParticipant = dict[str, Union[str, int, dict[str, str], list[str]]]


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


@transaction.atomic
def letter_create(
    *,
    current_user: User,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    letter_type: str,
    language: str,
    participants: Optional[list[LetterParticipant]] = None,
    attachments,
) -> Letter:
    letter_data = {
        "letter_type": letter_type,
        "subject": subject,
        "body": body,
        "current_state": Letter.States.DRAFT,
        "owner": current_user,
        "language": language,
    }

    letter_instance = create_letter_instance(**letter_data)

    if letter_type in ["internal", "outgoing"]:
        author_participant = OrderedDict({
            "id": "",
            "user_id": current_user.id,
            "role": 1,
            "participant_type": "user",
        })
        participants.append(author_participant)

    participants_create(current_user=current_user, letter_instance=letter_instance, participants=participants)

    letter_attachment_create(current_user=current_user, letter_instance=letter_instance, attachments=attachments)

    return letter_instance


@transaction.atomic
def letter_create_and_publish(
    *,
    current_user: User,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    letter_type: str,
    language: str,
    participants: Optional[list[LetterParticipant]] = None,
    attachments,
) -> Letter:
    letter_data = {
        "letter_type": letter_type,
        "subject": subject,
        "body": body,
        "current_state": Letter.States.DRAFT,
        "owner": current_user,
        "language": language,
    }

    letter_instance = create_letter_instance(**letter_data)

    letter_instance.current_state = Letter.States.SUBMITTED

    letter_instance.save()

    participants_create(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=participants,
    )

    letter_attachment_create(current_user=current_user, letter_instance=letter_instance, attachments=attachments)

    letter_publish(current_user=current_user, letter_instance=letter_instance)

    return letter_instance
