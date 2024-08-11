from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from core.comments.services import comment_create
from core.letters.models import Letter
from core.users.models import User

from .models import BaseParticipant
from .utils import get_enum_value, verify_owners_role

type LetterParticipant = dict[str, Union[str, int, dict[str, str], list[str]]]


@transaction.atomic
def participant_instance_create(
    current_user: User,
    target_user_id: str,
    user_type: str,
    letter_instance: Letter,
    role: int,
    permissions: list[str] = None,
):
    # user_instance_classes = {"User": User, "guest": Guest}.get(user_type)
    user_instance_classes = {"User": User}.get(user_type)

    if user_instance_classes == User:
        user = user_instance_classes.objects.get(pk=target_user_id)

        if role == BaseParticipant.Roles.ADMINISTRATOR and not user.is_staff:
            raise PermissionDenied("Cannot assign administrator privileges to a non-staff user.")

    # elif user_instance_classes == Guest:
    #     user, _ = user_instance_classes.objects.get_or_create(name=target_user_id)

    else:
        raise ValueError("Invalid user type")

    participant_instance = BaseParticipant.objects.create(
        user=user,
        role=role,
        letter=letter_instance,
        added_by=current_user,
    )

    participant_instance.save(permissions=permissions)


# This function create participants for a given letter.
@transaction.atomic
def participants_create(
    *,
    current_user: User,
    letter_instance: Letter,
    participants,
):
    participants = verify_owners_role(letter_instance=letter_instance, participants=participants)

    for participant in participants:
        role_value = get_enum_value(participant["role"])

        participant_instance_create(
            target_user_id=participant["user"]["id"],
            user_type=participant["user"]["user_type"],
            role=role_value,
            letter_instance=letter_instance,
            current_user=current_user,
        )

    return participants


def add_participants(
    *,
    current_user: User,
    letter_instance: Letter,
    participants: dict[str, Union[str, list[str]]],
):
    target_users_ids = participants["to"]

    for target_user_id in target_users_ids:
        participant_instance_create(
            target_user_id=target_user_id,
            user_type="User",
            role=participants.get("role", BaseParticipant.Roles.COLLABORATOR),
            letter_instance=letter_instance,
            current_user=current_user,
            permissions=participants.get("permissions"),
        )

    comment_create(
        current_user=current_user,
        letter_instance=letter_instance,
        body=participants.get("message"),
    )

    return


def remove_participants(
    *,
    current_user: User,
    letter_instance: Letter,
    participants: list[LetterParticipant],
):
    target_users_ids = participants["to"]
    role_value = get_enum_value(participants.get("role"))

    for target_user_id in target_users_ids:
        try:
            target_user = get_object_or_404(User, pk=target_user_id)
            participant_instance = letter_instance.participants.get(role=role_value, user=target_user)
        except ObjectDoesNotExist:
            continue

        participant_instance.delete()

    return
