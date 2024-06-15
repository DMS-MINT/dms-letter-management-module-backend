from django.core.exceptions import ValidationError

from core.permissions.models import Permission

from .models import Participant

ROLE_PERMISSIONS = {
    Participant.RoleNames.EDITOR: ["view", "edit", "comment"],
    Participant.RoleNames.AUTHOR: [
        "view",
        "edit",
        "comment",
        "share",
        "submit",
        "delete",
        "retract",
        "archive",
        "close",
    ],
    Participant.RoleNames.PRIMARY_RECIPIENT: ["view", "comment", "share"],
    Participant.RoleNames.CC: ["view", "comment"],
    Participant.RoleNames.BCC: ["view"],
}


def get_permissions(role):
    permission_names = ROLE_PERMISSIONS.get(role)
    if permission_names is None:
        raise ValidationError(f"Invalid role: {role}")

    return Permission.objects.filter(name__in=permission_names)
