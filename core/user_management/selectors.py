from core.users.models import User

from .filters import BaseMemberFilter
from .models import Member


def member_list(current_user=User, filters=None):
    filters = filters or {}

    qs = Member.objects.prefetch_related("member_profile", "member_permissions").all()

    return BaseMemberFilter(filters, qs, current_user=current_user).qs


def member_profile_details(*, member_id):
    return Member.objects.prefetch_related("member_profile", "member_permissions", "member_settings").get(
        id=member_id,
    )
