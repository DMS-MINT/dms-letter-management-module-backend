from core.letters.models import Letter
from core.participants.models import Participant
from core.users.models import Member


def get_permissions(*, current_user=Member, letter_instance: Letter):
    try:
        letter_actions = letter_instance.current_state.actions.all()

        participant_instance = letter_instance.participants.get(user=current_user, letter=letter_instance)
        participant_permissions = participant_instance.permissions.all()

        letter_actions_set = set(letter_actions.values_list("name", flat=True))
        participant_permissions_set = set(participant_permissions.values_list("name", flat=True))

        common_permissions = letter_actions_set & participant_permissions_set

        return {
            "can_edit": "edit" in common_permissions,
            "can_submit": "submit" in common_permissions,
            "can_comment": "comment" in common_permissions,
            "can_share": "share" in common_permissions,
            "can_delete": "delete" in common_permissions,
            "can_retract": "retract" in common_permissions,
            "can_archive": "archive" in common_permissions,
            "can_close": "close" in common_permissions,
            "can_publish": "publish" in common_permissions,
            "can_reject": "reject" in common_permissions,
        }

    except Participant.DoesNotExist:
        return None
    except AttributeError:
        return None
