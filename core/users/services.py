from typing import Optional

from core.departments.models import Department, JobTitle
from django.utils.crypto import get_random_string

from core.emails.services import email_send_type
from .models import User


def user_create(
    *,
    first_name_en: str,
    middle_name_en: str,
    last_name_en: str,
    first_name_am: str,
    middle_name_am: str,
    last_name_am: str,
    job_title: str,
    department: str,
    email: str,
    phone_number: str,
    is_active: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
    password: Optional[str] = None,
) -> User:
    department_instance = Department.objects.get(department_name_en=department)
    job_title_instance = JobTitle.objects.get(title_en=job_title)
        
    return (
        User.objects.create_user(
            first_name_en=first_name_en,
            middle_name_en=middle_name_en,
            last_name_en=last_name_en,
            first_name_am=first_name_am,
            middle_name_am=middle_name_am,
            last_name_am=last_name_am,
            job_title=job_title_instance,
            department=department_instance,
            email=email,
            phone_number=phone_number,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            password=password,
        ),
    )
