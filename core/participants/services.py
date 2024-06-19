from typing import Union

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from core.letters.models import Letter
from core.permissions.service import assign_permissions
from core.users.models import Guest, Member

from .models import Participant
from .utils import get_enum_value, verify_owners_role

type LetterParticipant = dict[str, Union[str, dict[str, str], list[str]]]


@transaction.atomic
def participant_instance_create(
    current_user: Member,
    user_id: str,
    user_type: str,
    letter_instance: Letter,
    role: int,
):
    user_instance_classes = {"member": Member, "guest": Guest}.get(user_type)

    if user_instance_classes:
        user = user_instance_classes.objects.get(pk=user_id)
        return Participant.objects.create(
            user=user,
            role=role,
            letter=letter_instance,
            added_by=current_user,
        )

    raise ValueError("Invalid user type")


# This function create participants for a given letter.
@transaction.atomic
def participants_create(
    *,
    current_user: Member,
    participants: list[LetterParticipant],
    letter_instance: Letter,
):
    participants = verify_owners_role(letter_instance=letter_instance, participants=participants)

    for participant in participants:
        role_value = get_enum_value(participant["role"])

        participant_instance = participant_instance_create(
            user_id=participant["user"]["id"],
            user_type=participant["user"]["user_type"],
            role=role_value,
            letter_instance=letter_instance,
            current_user=current_user,
        )

        assign_permissions(
            letter_instance=letter_instance,
            participant_user=participant_instance.user,
            participant_role=role_value,
            permissions=participant.get("permissions"),
        )

    return participants
