from django.db.models import Q

from .models import User


def user_get_users(current_user=User):
    members = User.objects.filter(Q(is_admin=False) & Q(is_superuser=False) & ~Q(id=current_user.id))

    # guests = Guest.objects.all()

    return list(members)
    # + list(guests)
