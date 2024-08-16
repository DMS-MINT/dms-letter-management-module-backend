from django.db.models import Q

from .models import User


def user_get_users(current_user=User):
    users = User.objects.filter(Q(is_admin=False) & Q(is_superuser=False) & ~Q(id=current_user.id))

    return list(users)
