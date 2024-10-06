def organization_detail(organization_instance):
    organization_profile = organization_instance.organization_profile.first()

    domains = [
        {
            "id": domain.id,
            "domain": domain.domain,
            "is_primary": domain.is_primary,
        }
        for domain in organization_instance.domains.all()
    ]

    return {
        "id": organization_instance.id,
        "name_en": organization_instance.name_en,
        "name_am": organization_instance.name_am,
        "domains": domains,
        "bio": organization_profile.bio,
        "contact_phone": organization_profile.contact_phone,
        "contact_email": organization_profile.contact_email,
        "address": {
            "city_en": organization_profile.address.city_en if organization_profile.address else None,
            "city_am": organization_profile.address.city_am if organization_profile.address else None,
        },
        "postal_code": organization_profile.postal_code,
        "logo": organization_profile.logo.url if organization_profile.logo else None,
        "created_at": organization_instance.created_at,
        "updated_at": organization_instance.updated_at,
    }
