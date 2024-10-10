from django.contrib import admin

from .models import Domain, Tenant, TenantProfile, TenantSetting


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ["name_en", "name_am"]
    search_fields = ["name_en", "name_am"]

    fieldsets = (
        (
            "Tenant Details",
            {
                "fields": ("name_en", "name_am", "database_name", "owner"),
            },
        ),
    )

    # Adding readonly_fields for fields that shouldn't be edited once set
    readonly_fields = ["database_name", "owner"]

    show_in_index = True


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = [
        "tenant",
        "contact_phone",
        "contact_email",
        "postal_code",
        "address",
    ]
    search_fields = [
        "contact_phone",
        "contact_email",
        "postal_code",
    ]

    fieldsets = (
        (
            "Tenant Profile Details",
            {
                "fields": (
                    "tenant",
                    "bio",
                    "contact_phone",
                    "contact_email",
                    "address",
                    "postal_code",
                    "logo",
                ),
            },
        ),
    )

    # Mark the logo as readonly if we want to prevent accidental changes
    readonly_fields = ["logo"]

    show_in_index = True


@admin.register(TenantSetting)
class TenantSettingAdmin(admin.ModelAdmin):
    list_display = ["tenant", "auto_ref_number_letters", "auto_date_letters"]

    fieldsets = (
        (
            "Settings",
            {
                "fields": (
                    "tenant",
                    "auto_ref_number_letters",
                    "auto_date_letters",
                ),
            },
        ),
    )

    show_in_index = True


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["domain", "tenant", "is_primary"]
    search_fields = ["domain"]

    fieldsets = (
        (
            "Domain Details",
            {
                "fields": ("domain", "tenant", "is_primary"),
            },
        ),
    )

    show_in_index = True
