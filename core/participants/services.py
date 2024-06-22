from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied

from core.comments.services import comment_create
from core.letters.models import Letter
from core.permissions.service import assign_permissions, remove_permissions
from core.users.models import Guest, Member

from .models import Participant
from .utils import get_enum_value, verify_owners_role

type LetterParticipant = dict[str, Union[str, int, dict[str, str], list[str]]]


@transaction.atomic
def participant_instance_create(
    current_user: Member,
    target_user_id: str,
    user_type: str,
    letter_instance: Letter,
    role: int = Participant.Roles.COLLABORATOR,
):
    user_instance_classes = {"member": Member, "guest": Guest}.get(user_type)

    if user_instance_classes:
        user = user_instance_classes.objects.get(pk=target_user_id)

        if role == Participant.Roles.ADMINISTRATOR and not user.is_staff:
            raise PermissionDenied("Cannot assign administrator privileges to a non-staff user.")

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
    letter_instance: Letter,
    participants: list[LetterParticipant],
):
    participants = verify_owners_role(letter_instance=letter_instance, participants=participants)

    for participant in participants:
        role_value = get_enum_value(participant["role"])

        participant_instance = participant_instance_create(
            target_user_id=participant["user"]["id"],
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


def add_participants(
    *,
    current_user: Member,
    letter_instance: Letter,
    participants: list[LetterParticipant],
):
    for participant in participants:
        target_users_ids = participant["to"]
        role_value = get_enum_value(participant.get("role"))

        for target_user_id in target_users_ids:
            participant_instance = participant_instance_create(
                target_user_id=target_user_id,
                user_type="member",
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

        if "message" in participant and participant["message"]:
            comment_create(
                current_user=participant_instance.user,
                letter_instance=letter_instance,
                content=participant.get("message"),
            )

    return participant


def remove_participants(
    *,
    current_user: Member,
    letter_instance: Letter,
    participants: list[LetterParticipant],
):
    for participant in participants:
        target_users_ids = participant["to"]
        role_value = get_enum_value(participant.get("role"))

        for target_user_id in target_users_ids:
            try:
                target_user = get_object_or_404(Member, pk=target_user_id)
                participant_instance = letter_instance.participants.get(role=role_value, user=target_user)
            except ObjectDoesNotExist:
                continue

            remove_permissions(
                letter_instance=letter_instance,
                participant_user=participant_instance.user,
                participant_role=role_value,
                permissions=participant.get("permissions"),
            )

            participant_instance.delete()
