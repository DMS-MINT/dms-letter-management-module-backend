from guardian.shortcuts import get_perms, get_users_with_perms
from rest_framework.exceptions import PermissionDenied

from core.letters.models import Letter


class ApiPermMixin:
    required_object_perms = []

    def get_required_object_perms(self):
        return self.required_object_perms

    def check_object_permissions(self, request, obj):
        required_perms = set(self.get_required_object_perms())
        user_perms = set(get_perms(request.user, obj))
        allowed_actions = set(self.get_allowed_actions(obj))

        if not required_perms.issubset(user_perms):
            raise PermissionDenied("You do not have permission to perform this action on this letter.")

        if not required_perms.issubset(allowed_actions):
            raise PermissionDenied("You can not perform this action on this letter in its current state..")

    def get_object_permissions(self, user, obj):
        user_perms = set(get_perms(user, obj))
        allowed_actions = set(self.get_allowed_actions(obj))

        return list(user_perms.intersection(allowed_actions))

    def get_object_permissions_details(self, obj):
        users_with_perms = get_users_with_perms(obj, attach_perms=True)
        formatted_data = []

        for user, permissions in users_with_perms.items():
            allowed_actions = set(self.get_allowed_actions(obj))
            user_permissions = set(permissions)

            intersected_permissions = list(user_permissions.intersection(allowed_actions))

            user_data = {
                "user_id": str(user.id),
                "permissions": intersected_permissions,
            }
            formatted_data.append(user_data)

        return formatted_data

    @staticmethod
    def get_allowed_actions(obj):
        current_state = obj.current_state
        state_permissions = {
            Letter.States.DRAFT: [
                # Basic Permissions
                "can_view_letter",
                "can_update_letter",
                "can_delete_letter",
                # Workflow Permissions
                "can_share_letter",
                "can_submit_letter",
                # Interaction Permissions
                "can_comment_letter",
            ],
            Letter.States.SUBMITTED: [
                # Basic Permissions
                "can_view_letter",
                # Workflow Permissions
                "can_share_letter",
                "can_publish_letter",
                "can_retract_letter",
                # Interaction Permissions
                "can_comment_letter",
            ],
            Letter.States.PUBLISHED: [
                # Basic Permissions
                "can_view_letter",
                # Workflow Permissions
                "can_share_letter",
                "can_retract_letter",
                "can_close_letter",
                # Interaction Permissions
                "can_comment_letter",
            ],
            Letter.States.CLOSED: [
                # Basic Permissions
                "can_view_letter",
                "can_archive_letter",
                # Workflow Permissions
                "can_share_letter",
                "can_reopen_letter",
            ],
        }

        return state_permissions.get(current_state, [])
