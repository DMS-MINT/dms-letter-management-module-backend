from .filters import BaseLetterFilter
from .models import Letter


def letter_list(*, filters=None):
    filters = filters or {}

    qs = Letter.objects.filter(participants__user_id="8e7365aa-f959-4514-be8b-cba84571a86c")

    return BaseLetterFilter(filters, qs).qs
