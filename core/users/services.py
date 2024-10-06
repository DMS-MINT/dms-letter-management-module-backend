from typing import Optional

from django.db import transaction

from core.departments.models import Department, JobTitle

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
    phone_number: int,
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
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            password=password,
        ),
    )


@transaction.atomic
def user_update(
    *,
    user: User,
    email: str = None,
    first_name_en: str = None,
    middle_name_en: str = None,
    last_name_en: str = None,
    first_name_am: str = None,
    middle_name_am: str = None,
    last_name_am: str = None,
    job_title: str = None,
    department: str = None,
    phone_number: int = None,
    is_staff: bool = None,
    is_superuser: bool = None,
) -> User:
    if email is not None:
        user.email = str(email)

    if is_staff is not None:
        user.is_staff = bool(is_staff)

    if is_superuser is not None:
        user.is_superuser = bool(is_superuser)

    user.save()

    user_profile = user.user_profile

    if first_name_en is not None:
        user_profile.first_name_en = str(first_name_en)

    if middle_name_en is not None:
        user_profile.middle_name_en = str(middle_name_en)

    if last_name_en is not None:
        user_profile.last_name_en = str(last_name_en)

    if first_name_am is not None:
        user_profile.first_name_am = str(first_name_am)

    if middle_name_am is not None:
        user_profile.middle_name_am = str(middle_name_am)

    if last_name_am is not None:
        user_profile.last_name_am = str(last_name_am)

    if job_title is not None:
        user_profile.job_title_id = str(job_title)

    if department is not None:
        user_profile.department_id = str(department)

    if phone_number is not None:
        user_profile.phone_number = int(phone_number)

    user_profile.save()

    return user
