import time

from django.conf import settings
from django.db import transaction
from rest_framework import status as http_status

from core.api.exceptions import APIError
from core.common.models import Address
from core.users.models import User

from .models import Domain, Tenant, TenantProfile, TenantSetting


@transaction.atomic
def tenant_create(
    tenant_slug: str,
    current_user: User,
    *,
    name_en: str,
    name_am: str,
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

    TenantSetting.objects.create(
        tenant=tenant_instance,
    )

    return tenant_instance.id


@transaction.atomic
def tenant_profile_update(
    *,
    tenant_instance: Tenant,
    name_en: str = None,
    name_am: str = None,
    bio: str = None,
    contact_phone: int = None,
    contact_email: str = None,
    postal_code: int = None,
    address: dict = None,
    logo=None,
):
    if name_en is not None:
        tenant_instance.name_en = name_en

    if name_am is not None:
        tenant_instance.name_am = name_am

    if bio is not None:
        tenant_instance.tenant_profile.bio = bio

    if contact_phone is not None:
        tenant_instance.tenant_profile.contact_phone = contact_phone

    if contact_email is not None:
        tenant_instance.tenant_profile.contact_email = contact_email

    if postal_code is not None:
        tenant_instance.tenant_profile.postal_code = postal_code

    if address is not None:
        tenant_instance.tenant_profile.address.city_en = address.get(
            "city_en",
            tenant_instance.tenant_profile.address.city_en,
        )
        tenant_instance.tenant_profile.address.city_am = address.get(
            "city_am",
            tenant_instance.tenant_profile.address.city_am,
        )

    if logo is not None:
        tenant_instance.tenant_profile.logo = logo

    tenant_instance.tenant_profile.save()
    tenant_instance.save()

    return tenant_instance


@transaction.atomic
def set_or_update_tenant_settings(
    *,
    tenant_instance: Tenant,
    auto_ref_number_letters: bool = None,
    auto_date_letters: bool = None,
):
    if auto_ref_number_letters is not None:
        tenant_instance.tenant_settings.auto_ref_number_letters = auto_ref_number_letters

    if auto_date_letters is not None:
        tenant_instance.tenant_settings.auto_date_letters = auto_date_letters

    tenant_instance.tenant_settings.save()
