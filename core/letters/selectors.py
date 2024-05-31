from .filters import BaseLetterFilter
from .models import Letter


def letter_list(*, filters=None):
    filters = filters or {}

    qs = Letter.objects.filter(participants__user_id="d691069e-f7f6-44d4-9443-7b85f0234f19")

    return BaseLetterFilter(filters, qs).qs
