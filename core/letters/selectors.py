from core.users.models import Member

from .filters import BaseLetterFilter
from .models import Letter


def letter_list(*, current_user=Member, filters=None):
    filters = filters or {}
    print(filters)

    qs = Letter.objects.all()

    return qs
    # return BaseLetterFilter(filters, qs, current_user=current_user).qs
