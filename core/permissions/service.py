from guardian.shortcuts import assign_perm, remove_perm

from core.letters.models import Letter
from core.participants.models import Participant


def assign_permissions(
    *,
    letter_instance: Letter,
    participant_user,
    participant_role: int,
    permissions: list[str] = None,
):
    assign_perm("can_view_letter", participant_user, letter_instance)
    match participant_role:
        case Participant.Roles.AUTHOR.value:
            # Basic Permissions
            assign_perm("can_update_letter", participant_user, letter_instance)
            assign_perm("can_delete_letter", participant_user, letter_instance)
            assign_perm("can_archive_letter", participant_user, letter_instance)
            # Workflow Permissions
            assign_perm("can_share_letter", participant_user, letter_instance)
            assign_perm("can_submit_letter", participant_user, letter_instance)
            assign_perm("can_retract_letter", participant_user, letter_instance)
            assign_perm("can_close_letter", participant_user, letter_instance)
            assign_perm("can_reopen_letter", participant_user, letter_instance)
            # Interaction Permissions
            assign_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.Roles.PRIMARY_RECIPIENT.value:
            # Workflow Permissions
            assign_perm("can_share_letter", participant_user, letter_instance)
            assign_perm("can_close_letter", participant_user, letter_instance)
            # Interaction Permissions
            assign_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.Roles.CC.value:
            # Interaction Permissions
            assign_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.Roles.COLLABORATOR.value:
            if permissions is not None:
                for permission in permissions:
                    assign_perm(permission, participant_user, letter_instance)
        case Participant.Roles.ADMINISTRATOR.value:
            # Workflow Permissions
            if participant_user.is_staff:
                assign_perm("can_retract_letter", participant_user, letter_instance)
        case _:
            return


def remove_permissions(
    *,
    letter_instance: Letter,
    participant_user,
    participant_role: int,
    permissions: list[str] = None,
):
    remove_perm("can_view_letter", participant_user, letter_instance)
    match participant_role:
        case Participant.Roles.AUTHOR.value:
            # Basic Permissions
            remove_perm("can_update_letter", participant_user, letter_instance)
            remove_perm("can_delete_letter", participant_user, letter_instance)
            remove_perm("can_archive_letter", participant_user, letter_instance)
            # Workflow Permissions
            remove_perm("can_share_letter", participant_user, letter_instance)
            remove_perm("can_submit_letter", participant_user, letter_instance)
            remove_perm("can_retract_letter", participant_user, letter_instance)
            remove_perm("can_close_letter", participant_user, letter_instance)
            remove_perm("can_reopen_letter", participant_user, letter_instance)
            # Interaction Permissions
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.Roles.PRIMARY_RECIPIENT.value:
            # Workflow Permissions
            remove_perm("can_share_letter", participant_user, letter_instance)
            remove_perm("can_close_letter", participant_user, letter_instance)
            # Interaction Permissions
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.Roles.CC.value:
            # Interaction Permissions
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Participant.Roles.COLLABORATOR.value:
            if permissions is not None:
                for permission in permissions:
                    remove_perm(permission, participant_user, letter_instance)
        case Participant.Roles.ADMINISTRATOR.value:
            # Workflow Permissions
            if participant_user.is_staff:
                remove_perm("can_retract_letter", participant_user, letter_instance)
        case _:
            return


def grant_owner_permissions(letter_instance: Letter):
    assign_perm("can_view_letter", letter_instance.owner, letter_instance)
    assign_perm("can_update_letter", letter_instance.owner, letter_instance)
    assign_perm("can_delete_letter", letter_instance.owner, letter_instance)
    assign_perm("can_archive_letter", letter_instance.owner, letter_instance)
    assign_perm("can_share_letter", letter_instance.owner, letter_instance)
    assign_perm("can_comment_letter", letter_instance.owner, letter_instance)


def remove_owner_permissions(letter_instance: Letter):
    remove_perm("can_view_letter", letter_instance.owner, letter_instance)
    remove_perm("can_update_letter", letter_instance.owner, letter_instance)
    remove_perm("can_delete_letter", letter_instance.owner, letter_instance)
    remove_perm("can_archive_letter", letter_instance.owner, letter_instance)
    remove_perm("can_share_letter", letter_instance.owner, letter_instance)
    remove_perm("can_comment_letter", letter_instance.owner, letter_instance)
