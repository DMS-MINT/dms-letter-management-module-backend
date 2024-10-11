from core.common.utils import get_object
from core.user_management.models import Member, UserPermissions

from .middleware import set_db_for_router
from .models import Tenant


def list_user_tenants(*, user_id: str, tenants):
    return [tenant_detail(user_id=user_id, tenant_instance=tenant) for tenant in tenants]


def tenant_detail(*, user_id: str, tenant_instance: Tenant):
    tenant_profile = tenant_instance.tenant_profile

    db = tenant_instance.database_name

    set_db_for_router("tenant")
    member = get_object(Member, user_id=user_id)
    user_permissions = get_object(UserPermissions, member=member)

    domains = [
        {
            "id": domain.id,
            "domain": domain.domain,
            "is_primary": domain.is_primary,
        }
        for domain in tenant_instance.domains.all()
    ]

    return {
        "id": tenant_instance.id,
        "name_en": tenant_instance.name_en,
        "name_am": tenant_instance.name_am,
        "domains": domains,
        "bio": tenant_profile.bio,
        "contact_phone": tenant_profile.contact_phone,
        "contact_email": tenant_profile.contact_email,
        "address": {
            "city_en": tenant_profile.address.city_en if tenant_profile.address else None,
            "city_am": tenant_profile.address.city_am if tenant_profile.address else None,
        },
        "postal_code": tenant_profile.postal_code,
        "logo": tenant_profile.logo.url if tenant_profile.logo else None,
        "created_at": tenant_instance.created_at,
        "updated_at": tenant_instance.updated_at,
        "permissions": {
            "is_admin": user_permissions.is_admin,
            "is_staff": user_permissions.is_staff,
            "is_superuser": user_permissions.is_superuser,
        },
    }
