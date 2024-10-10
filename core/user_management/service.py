from core.tenants.models import Tenant
from core.users.models import User

from .models import Member, UserPermissions


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
