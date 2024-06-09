from core.users.models import Member

from .filters import BaseLetterFilter
from .models import Letter


def letter_list(*, user=Member, filters=None):
    filters = filters or {}

    qs = Letter.objects.filter(participants__user_id=user.id)

    return BaseLetterFilter(filters, qs).qs
