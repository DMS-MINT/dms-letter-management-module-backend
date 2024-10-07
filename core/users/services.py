from typing import Optional

from django.db import transaction
from django_tenants.utils import get_public_schema_name, schema_context
from tenant_users.tenants.utils import get_current_tenant

from core.user_management.models import UserProfile

from .models import User


def user_create(
    *,
    email: str,
    password: Optional[str] = None,
    first_name_en: str,
    middle_name_en: str,
    last_name_en: str,
    first_name_am: str,
    middle_name_am: str,
    last_name_am: str,
    job_title: str,
    department: str,
    phone_number: int,
    is_staff: bool = False,
    is_superuser: bool = False,
) -> User:
    current_org = get_current_tenant()

    with schema_context(get_public_schema_name()):
        user_instance = User.objects.create_user(
            email=email,
            password=password,
            is_active=True,
        )

    UserProfile.objects.create(
        user=user_instance,
        first_name_en=first_name_en,
        middle_name_en=middle_name_en,
        last_name_en=last_name_en,
        first_name_am=first_name_am,
        middle_name_am=middle_name_am,
        last_name_am=last_name_am,
        job_title_id=job_title,
        department_id=department,
        phone_number=phone_number,
    )

    current_org.add_user(user_instance, is_superuser=is_superuser, is_staff=is_staff)

    return user_instance


@transaction.atomic
def user_update(
    *,
    user_instance: User,
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
        user_instance.email = str(email)

    if is_staff is not None:
        user_instance.is_staff = bool(is_staff)

    if is_superuser is not None:
        user_instance.is_superuser = bool(is_superuser)

    user_instance.save()

    user_profile = user_instance.user_profile.first()

    if user_profile is None:
        user_profile = UserProfile.objects.create(
            user=user_instance,
            first_name_en=first_name_en,
            middle_name_en=middle_name_en,
            last_name_en=last_name_en,
            first_name_am=first_name_am,
            middle_name_am=middle_name_am,
            last_name_am=last_name_am,
            job_title_id=job_title,
            department_id=department,
            phone_number=phone_number,
        )
    else:
        if first_name_en is not None:
            user_profile.first_name_en = first_name_en

        if middle_name_en is not None:
            user_profile.middle_name_en = middle_name_en

        if last_name_en is not None:
            user_profile.last_name_en = last_name_en

        if first_name_am is not None:
            user_profile.first_name_am = first_name_am

        if middle_name_am is not None:
            user_profile.middle_name_am = middle_name_am

        if last_name_am is not None:
            user_profile.last_name_am = last_name_am

        if job_title is not None:
            user_profile.job_title_id = job_title

        if department is not None:
            user_profile.department_id = department

        if phone_number is not None:
            user_profile.phone_number = phone_number

    user_profile.save()

    return user_instance
