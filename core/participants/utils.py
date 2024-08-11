from typing import Union

from django.core.exceptions import BadRequest

from .models import BaseParticipant

type LetterParticipant = dict[str, Union[str, dict[str, str]]]


def get_enum_value(key: str) -> int:
    for role in BaseParticipant.Roles:
        if role.label.lower() == key.lower():
            return role.value
    raise ValueError(f"No matching participant role value for key: {key}")


def verify_owners_role(*, letter_instance, participants):
    owner_exists = next(
        (participant for participant in participants if participant["user"]["id"] == letter_instance.owner),
        None,
    )

    if owner_exists:
        role_value = get_enum_value(owner_exists["role"])

        if role_value not in [BaseParticipant.Roles.AUTHOR, BaseParticipant.Roles.COLLABORATOR]:
            raise BadRequest("As the owner of the letter, you cannot be a recipient of the same letter.")

    return participants


def identify_participants_changes(letter_instance, new_participants):
    existing_participants_ids = set(letter_instance.participants.values_list("id", flat=True))
    new_participants_ids = set(participant["id"] for participant in new_participants)

    participants_to_remove_ids = existing_participants_ids - new_participants_ids
    participants_to_add_ids = new_participants_ids - existing_participants_ids

    participants_to_add = [
        participant for participant in new_participants if participant["id"] in participants_to_add_ids
    ]

    participants_to_remove = letter_instance.participants.filter(id__in=participants_to_remove_ids)

    return participants_to_add, participants_to_remove


def update_creator_role_on_remove():
    pass
