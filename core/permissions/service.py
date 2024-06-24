from enum import Enum

from guardian.shortcuts import assign_perm, remove_perm

from core.letters.models import Letter


class Roles(Enum):
    AUTHOR = 1
    PRIMARY_RECIPIENT = 2
    CC = 3
    BCC = 4
    COLLABORATOR = 5
    ADMINISTRATOR = 6


def assign_permissions(
    *,
    letter_instance: Letter,
    participant_user,
    participant_role: int,
    permissions: list[str] = None,
):
    assign_perm("can_view_letter", participant_user, letter_instance)
    match participant_role:
        case Roles.AUTHOR.value:
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
        case Roles.PRIMARY_RECIPIENT.value:
            # Workflow Permissions
            assign_perm("can_share_letter", participant_user, letter_instance)
            assign_perm("can_close_letter", participant_user, letter_instance)
            assign_perm("can_reopen_letter", participant_user, letter_instance)
            # Interaction Permissions
            assign_perm("can_comment_letter", participant_user, letter_instance)
        case Roles.CC.value:
            # Interaction Permissions
            assign_perm("can_comment_letter", participant_user, letter_instance)
        case Roles.COLLABORATOR.value:
            if permissions is not None:
                for permission in permissions:
                    assign_perm(permission, participant_user, letter_instance)
        case Roles.ADMINISTRATOR.value:
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
        case Roles.AUTHOR.value:
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
        case Roles.PRIMARY_RECIPIENT.value:
            # Workflow Permissions
            remove_perm("can_share_letter", participant_user, letter_instance)
            remove_perm("can_close_letter", participant_user, letter_instance)
            remove_perm("can_reopen_letter", participant_user, letter_instance)
            # Interaction Permissions
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Roles.CC.value:
            # Interaction Permissions
            remove_perm("can_comment_letter", participant_user, letter_instance)
        case Roles.COLLABORATOR.value:
            if permissions is not None:
                for permission in permissions:
                    remove_perm(permission, participant_user, letter_instance)
        case Roles.ADMINISTRATOR.value:
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
