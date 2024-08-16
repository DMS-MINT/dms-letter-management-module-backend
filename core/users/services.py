from typing import Optional

from core.departments.models import Department

from .models import User


def user_create(
    *,
    first_name: str,
    last_name: str,
    job_title: str,
    department: str,
    email: str,
    phone_number: str,
    is_active: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
    password: Optional[str] = None,
) -> User:
    department_instance = Department.objects.get(name_en=department)

    return (
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            job_title=job_title,
            department=department_instance,
            email=email,
            phone_number=phone_number,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            password=password,
        ),
    )
