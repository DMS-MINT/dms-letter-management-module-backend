from .models import Member


def user_get_login_data(*, user: Member):
    return {
        "id": getattr(user, "id", ""),
        "email": getattr(user, "email", ""),
        "username": getattr(user, "username", ""),
        "first_name": getattr(user, "first_name", ""),
        "last_name": getattr(user, "last_name", ""),
        "full_name": getattr(user, "full_name", ""),
        "job_title": getattr(user, "job_title", ""),
        "department": getattr(user, "department", ""),
        "phone_number": getattr(user, "phone_number", ""),
    }
