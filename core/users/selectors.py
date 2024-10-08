from .filters import BaseUserFilter
from .models import User


def user_get_users(current_user=User, filters=None):
    filters = filters or {}

    qs = User.objects.prefetch_related("user_profile").all()

    return BaseUserFilter(filters, qs).qs
