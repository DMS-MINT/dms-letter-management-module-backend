import time

from django.conf import settings
from rest_framework import status as http_status

from core.api.exceptions import APIError
from core.common.models import Address
from core.users.models import User

from .models import Domain, Tenant, TenantProfile


def tenant_create(
    tenant_slug: str,
    current_user: User,
    *,
    name_en: str,
    name_am: str,
    is_staff: bool = False,
    is_superuser: bool = True,
    bio: str = None,
    contact_phone: int = None,
    contact_email: str = None,
    postal_code: int = None,
    address: dict = None,
    logo=None,
):
    if not current_user.is_active:
        raise APIError(
            error_code="INACTIVE_USER",
            status_code=http_status.HTTP_400_BAD_REQUEST,
            message="Inactive user can't be used to provision a tenant.",
            extra={},
        )

    tenant_primary_domain = f"{tenant_slug}.{settings.APP_DOMAIN}"
    tenant_admin_domain = f"{tenant_slug}.admin.{settings.APP_DOMAIN}"

    if Domain.objects.filter(domain=tenant_primary_domain).exists():
        raise APIError(
            error_code="TENANT_DOMAIN_EXISTS",
            status_code=http_status.HTTP_400_BAD_REQUEST,
            message="Tenant domain already exists.",
            extra={},
        )

    time_string = str(int(time.time()))
    database_name = f"{tenant_slug}_{time_string}"

    tenant_instance = Tenant.objects.create(
        slug=tenant_slug,
        database_name=database_name,
        owner=current_user,
        name_en=name_en,
        name_am=name_am,
    )

    # Create a domain associated with the organization and mark as primary
    Domain.objects.create(domain=tenant_primary_domain, tenant=tenant_instance, is_primary=True)
    Domain.objects.create(domain=tenant_admin_domain, tenant=tenant_instance, is_primary=False)

    address_instance, _ = Address.objects.get_or_create(
        city_en=address.get("city_en"),
        city_am=address.get("city_am"),
    )

    TenantProfile.objects.create(
        tenant=tenant_instance,
        bio=bio,
        address=address_instance,
        contact_phone=contact_phone,
        contact_email=contact_email,
        postal_code=postal_code,
        logo=logo,
    )

    return tenant_instance.id
