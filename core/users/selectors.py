from django.db.models import Q

from .models import Guest, Member


def user_get_users(current_user=Member):
    members = Member.objects.filter(Q(is_admin=False) & Q(is_superuser=False) & ~Q(id=current_user.id))

    guests = Guest.objects.all()

    return list(members) + list(guests)
