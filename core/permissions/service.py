from django.core.exceptions import ObjectDoesNotExist
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework.exceptions import PermissionDenied

from core.letters.models import Letter
from core.participants.models import Participant
from core.users.models import Member

from .models import Permission


def check_permissions(letter_instance, user, actions: list):
    for action in actions:
        action = action.lower()
        if not Permission.objects.filter(name=action).exists():
            raise ObjectDoesNotExist(f"{action} does not exist.")

        letter_participants = letter_instance.participants.filter(user=user)

        if not letter_participants.exists():
            raise PermissionDenied("You are not a participant in this letter.")

        if not letter_instance.current_state.can(action):
            raise PermissionDenied(f"The letter cannot be {action} in its current state.")

        if not any(participant.can(action) for participant in letter_participants):
            raise PermissionDenied(f"You do not have permission to {action} this letter.")

    return True


def assign_permissions(
    *,
    current_user: Member,
    letter_instance: Letter,
    participant_user,
    participant_role=Participant.RoleNames.COLLABORATOR,
    permissions: list[str] = None,
):
    assign_perm("can_view_letter", participant_user, letter_instance)
    match participant_role:
        case Participant.RoleNames.AUTHOR:
            assign_perm("can_update_letter", participant_user, letter_instance)
            assign_perm("can_delete_letter", participant_user, letter_instance)
            assign_perm("can_archive_letter", participant_user, letter_instance)
            assign_perm("can_share_letter", participant_user, letter_instance)
            assign_perm("can_submit_letter", participant_user, letter_instance)
            assign_perm("can_retract_letter", participant_user, letter_instance)
            assign_perm("can_close_letter", participant_user, letter_instance)
            assign_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.RoleNames.PRIMARY_RECIPIENT:
            assign_perm("can_share_letter", participant_user, letter_instance)
            assign_perm("can_close_letter", participant_user, letter_instance)
            assign_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.RoleNames.CC:
            assign_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.RoleNames.BCC:
            pass
        case Participant.RoleNames.COLLABORATOR:
            if permissions is not None:
                for permission in permissions:
                    assign_perm(permission, participant_user, letter_instance)
        case _:
            return


def remove_permissions(
    *,
    current_user: Member,
    letter_instance: Letter,
    participant_user,
    participant_role=Participant.RoleNames.COLLABORATOR,
    permissions=None,
):
    assign_perm("can_view_letter", participant_user, letter_instance)
    match participant_role:
        case Participant.RoleNames.AUTHOR:
            remove_perm("can_view_letter", participant_user, letter_instance)
            remove_perm("can_update_letter", participant_user, letter_instance)
            remove_perm("can_delete_letter", participant_user, letter_instance)
            remove_perm("can_archive_letter", participant_user, letter_instance)
            remove_perm("can_share_letter", participant_user, letter_instance)
            remove_perm("can_submit_letter", participant_user, letter_instance)
            remove_perm("can_retract_letter", participant_user, letter_instance)
            remove_perm("can_close_letter", participant_user, letter_instance)
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.RoleNames.PRIMARY_RECIPIENT:
            remove_perm("can_view_letter", participant_user, letter_instance)
            remove_perm("can_share_letter", participant_user, letter_instance)
            remove_perm("can_close_letter", participant_user, letter_instance)
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.RoleNames.CC:
            remove_perm("can_view_letter", participant_user, letter_instance)
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.RoleNames.BCC:
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.RoleNames.COLLABORATOR:
            if permissions is not None:
                for permission in permissions:
                    assign_perm(permission, participant_user, letter_instance)
        case _:
            return
