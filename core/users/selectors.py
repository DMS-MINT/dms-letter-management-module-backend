from django.db.models import Q

from .models import Guest, Member


def user_get_suggestions():
    members = Member.objects.filter(Q(is_admin=False) & Q(is_superuser=False))

    guests = Guest.objects.all()

    return list(members) + list(guests)
