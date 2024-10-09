def tenant_detail(tenant_instance):
    tenant_profile = tenant_instance.tenant_profile.first()

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
    }
