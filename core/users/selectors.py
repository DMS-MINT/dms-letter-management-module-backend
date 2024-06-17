from django.db.models import Q

from .models import Guest, Member


def user_get_login_data(*, user: Member):
    department = user.department.name
    return {
        "id": getattr(user, "id", ""),
        "email": getattr(user, "email", ""),
        "username": getattr(user, "username", ""),
        "first_name": getattr(user, "first_name", ""),
        "last_name": getattr(user, "last_name", ""),
        "full_name": getattr(user, "full_name", ""),
        "job_title": getattr(user, "job_title", ""),
        "department": department,
        "phone_number": getattr(user, "phone_number", ""),
    }


def user_get_suggestions():
    members = Member.objects.filter(Q(is_admin=False) & Q(is_superuser=False))

    guests = Guest.objects.all()

    return list(members) + list(guests)
