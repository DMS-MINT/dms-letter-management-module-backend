from core.users.models import Member


def user_get_login_data(*, current_user: Member):
    department = current_user.department

    return {
        "id": getattr(current_user, "id", ""),
        "email": getattr(current_user, "email", ""),
        "first_name": getattr(current_user, "first_name", ""),
        "last_name": getattr(current_user, "last_name", ""),
        "full_name": getattr(current_user, "full_name", ""),
        "job_title": getattr(current_user, "job_title", ""),
        "department": {
            "name_en": getattr(department, "name_en", ""),
            "name_am": getattr(department, "name_am", ""),
            "abbreviation_en": getattr(department, "abbreviation_en", ""),
            "abbreviation_am": getattr(department, "abbreviation_am", ""),
            "description": getattr(department, "description", ""),
            "contact_phone": getattr(department, "contact_phone", None),
            "contact_email": getattr(department, "contact_email", ""),
        },
        "phone_number": getattr(current_user, "phone_number", ""),
        "is_staff": getattr(current_user, "is_staff", False),
        "is_2fa_enabled": getattr(current_user, "is_2fa_enabled", False),
    }
