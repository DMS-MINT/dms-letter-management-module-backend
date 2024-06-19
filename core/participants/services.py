from typing import OrderedDict, Union

from django.core.exceptions import BadRequest, ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from core.letters.models import Letter
from core.permissions.models import Permission
from core.permissions.service import assign_permissions
from core.users.models import Guest, Member

from .models import Participant
from .utils import get_enum_value, verify_and_assign_permissions_to_creator

type LetterParticipant = dict[str, Union[str, dict[str, str], list[str]]]


@transaction.atomic
def participant_create(
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
def initialize_participants(
    *,
    current_user: Member,
    participants: list[LetterParticipant],
    letter_instance: Letter,
):
    participants = verify_and_assign_permissions_to_creator(
        current_user=current_user,
        participants=participants,
        letter_instance=letter_instance,
    )

    for participant in participants:
        role_value = get_enum_value(participant["role"])

        participant_instance = participant_create(
            user_id=participant["user"]["id"],
            user_type=participant["user"]["user_type"],
            role=role_value,
            letter_instance=letter_instance,
            current_user=current_user,
        )

        assign_permissions(
            current_user=current_user,
            letter_instance=letter_instance,
            participant_user=participant_instance.user,
            participant_role=role_value,
            permissions=participant.get("permissions"),
        )

    return participants


# This function updates participants for a given letter.
@transaction.atomic
def update_participants(*, current_user: Member, letter_instance, participants_to_add):
    if participants_to_add:
        for participant in participants_to_add:
            role = get_enum_value(participant["role"])
            user_data = participant["user"]

            if user_data["user_type"] == "member":
                user = Member.objects.get(pk=user_data["id"])
                if user == current_user:
                    if role == Participant.RoleNames.AUTHOR:
                        Participant.objects.get(letter=letter_instance, user=user).delete()
                        Participant.objects.create(
                            letter=letter_instance,
                            user=user,
                            role=Participant.RoleNames.AUTHOR,
                        )
                        return

                    raise ValidationError("You cannot send a letter to yourself as a recipient.")

            elif user_data["user_type"] == "guest":
                user, _ = Guest.objects.get_or_create(name=user_data["name"])

            Participant.objects.create(user=user, role=role, letter=letter_instance)
    return


# This function adds participants for a given letter.
@transaction.atomic
def participant_add(*, user: Member, letter_instance: Letter, permissions: list[str]):
    role = Participant.RoleNames.COLLABORATOR

    permission_objects = Permission.objects.filter(name__in=permissions)
    if permission_objects.count() != len(permissions):
        missing_permissions = set(permissions) - set(permission_objects.values_list("name", flat=True))
        raise ValueError(f"Invalid permission names: {missing_permissions}")

    participant_instance = letter_instance.participants.filter(user=user).first()

    if participant_instance is not None:
        current_permissions = set(participant_instance.permissions.values_list("name", flat=True))
        new_permissions = set(permission_objects.values_list("name", flat=True))

        combined_permissions = current_permissions.union(new_permissions)

        participant_instance.permissions.set(Permission.objects.filter(name__in=combined_permissions))
    else:
        participant_instance = Participant.objects.create(
            user=user,
            role=role,
            letter=letter_instance,
        )
        participant_instance.permissions.set(permission_objects)

    return participant_instance
