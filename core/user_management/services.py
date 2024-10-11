from typing import Optional

from django.db import transaction

from core.common.utils import get_object
from core.tenants.models import Tenant
from core.users.models import User

from .models import Member, UserPermissions, UserPreference, UserProfile, UserSetting


def set_or_update_user_permissions(
    *,
    user_id: str,
    is_admin: bool = None,
    is_staff: bool = None,
    is_superuser: bool = None,
):
    member_instance, _ = Member.objects.get_or_create(user_id=user_id)

    user_permissions, _ = UserPermissions.objects.get_or_create(member=member_instance)

    user_permissions.is_admin = is_admin
    user_permissions.is_staff = is_staff
    user_permissions.is_superuser = is_superuser
    user_permissions.save()

    return user_permissions


def add_user(
    *,
    current_user: User,
    tenant_instance: Tenant,
    is_admin: bool = None,
    is_staff: bool = None,
    is_superuser: bool = None,
):
    current_user.tenants.add(tenant_instance)

    set_or_update_user_permissions(
        user_id=current_user.id,
        is_admin=is_admin,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )


@transaction.atomic
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
    is_admin: bool = False,
    is_staff: bool = False,
) -> Member:
    existing_user = User.objects.filter(email=email).first()

    if not existing_user:
        user_instance = User.objects.create_user(email=email, password=password)
    else:
        user_instance = existing_user

    member_instance, _ = Member.objects.get_or_create(user_id=user_instance.id)

    UserProfile.objects.get_or_create(
        member=member_instance,
        defaults={
            "first_name_en": first_name_en,
            "middle_name_en": middle_name_en,
            "last_name_en": last_name_en,
            "first_name_am": first_name_am,
            "middle_name_am": middle_name_am,
            "last_name_am": last_name_am,
            "job_title_id": job_title,
            "department_id": department,
            "phone_number": phone_number,
        },
    )

    tenant_instance = get_object(Tenant, slug="mint")

    add_user(
        current_user=user_instance,
        tenant_instance=tenant_instance,
        is_admin=is_admin,
        is_staff=is_staff,
        is_superuser=False,
    )

    UserPermissions.objects.get_or_create(
        member=member_instance,
        defaults={
            "is_admin": is_admin,
            "is_staff": is_staff,
        },
    )

    UserSetting.objects.get_or_create(member=member_instance)

    UserPreference.objects.get_or_create(member=member_instance)

    return member_instance


@transaction.atomic
def member_update(
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
    is_admin: bool = None,
    is_staff: bool = None,
    is_superuser: bool = None,
) -> Member:
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
