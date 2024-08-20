from django.db.models import Q

from .models import User


def user_get_users(current_user=User, filters=None):
    is_staff = filters.get("is_staff")

    if not is_staff:
        users = User.objects.filter(
            Q(is_admin=False) & Q(is_superuser=False) & ~Q(id=current_user.id) & ~Q(is_staff=True),
        )
        return list(users)

    users = User.objects.filter(
        Q(is_admin=False) & Q(is_superuser=False) & ~Q(id=current_user.id) & Q(is_staff=is_staff),
    )

    return list(users)
