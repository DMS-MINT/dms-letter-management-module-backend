from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from core.contacts.services import contact_create
from core.enterprises.models import Enterprise
from core.letters.models import Letter
from core.users.models.user import User

from .models import BaseParticipant, EnterpriseParticipant, ExternalUserParticipant, InternalUserParticipant
from .utils import get_enum_value

type LetterParticipant = dict[str, Union[str, int, dict[str, str], list[str]]]


@transaction.atomic
def participant_instance_create(
    role: int,
    participant,
    current_user: User,
    letter_instance: Letter,
    permissions: list[str] = None,
):
    participant_type = participant.pop("participant_type")

    if participant_type == "user":
        user = User.objects.get(pk=participant["user_id"])

        if role == BaseParticipant.Roles.ADMINISTRATOR and not user.is_staff:
            raise PermissionDenied("Cannot assign administrator privileges to a non-staff user.")

        participant_instance = InternalUserParticipant.objects.create(
            user=user,
            role=role,
            letter=letter_instance,
            added_by=current_user,
        )

        participant_instance.save(permissions=permissions)

    elif participant_type == "enterprise":
        enterprise = Enterprise.objects.get(pk=participant["enterprise_id"])

        participant_instance = EnterpriseParticipant.objects.create(
            enterprise=enterprise,
            role=role,
            letter=letter_instance,
            added_by=current_user,
        )

    elif participant_type == "contact":
        contact = contact_create(
            current_user=current_user,
            full_name_en=participant["contact"]["full_name_en"],
            full_name_am=participant["contact"]["full_name_am"],
            email=participant["contact"]["email"],
            phone_number=participant["contact"]["phone_number"],
            address=participant["contact"]["address"],
        )

        participant_instance = ExternalUserParticipant.objects.create(
            contact=contact,
            role=role,
            letter=letter_instance,
            added_by=current_user,
        )

    else:
        raise ValueError("Invalid participant type. The allowed types are user, enterprise, or contact.")


# This function create participants for a given letter.
@transaction.atomic
def participants_create(
    *,
    current_user: User,
    letter_instance: Letter,
    participants: list[LetterParticipant],
    permissions: list[str] = None,
):
    # participants = verify_owners_role(letter_instance=letter_instance, participants=participants)

    for participant in participants:
        participant_instance_create(
            role=participant.pop("role"),
            participant=participant,
            letter_instance=letter_instance,
            current_user=current_user,
            permissions=permissions,
        )

    return participants


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
