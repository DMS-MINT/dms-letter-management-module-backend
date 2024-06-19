from typing import OrderedDict, Union

from django.core.exceptions import BadRequest

from .models import Participant

type LetterParticipant = dict[str, Union[str, dict[str, str]]]


def get_enum_value(key: str) -> int:
    for role in Participant.RoleNames:
        if role.label.lower() == key.lower():
            return role.value
    raise ValueError(f"No matching participant role value for key: {key}")


def verify_and_assign_permissions_to_creator(*, current_user, participants, letter_instance):
    current_user_exists = next(
        (participant for participant in participants if participant["user"]["id"] == current_user.id),
        None,
    )

    if current_user_exists:
        role_value = get_enum_value(current_user_exists["role_name"])
        if role_value not in [Participant.RoleNames.AUTHOR, Participant.RoleNames.COLLABORATOR]:
            raise BadRequest("You can't send a letter to yourself")
    else:
        new_participant = OrderedDict({
            "user": OrderedDict({"id": current_user.id, "user_type": "member"}),
            "role": Participant.RoleNames.COLLABORATOR.label,
        })

        if letter_instance.letter_type == "incoming":
            new_participant["permissions"] = [
                "can_update_letter",
                "can_delete_letter",
                "can_archive_letter",
                "can_share_letter",
                "can_submit_letter",
                "can_retract_letter",
                "can_close_letter",
                "can_comment_letter",
            ]

        participants.append(new_participant)

    return participants
