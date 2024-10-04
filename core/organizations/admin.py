from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from core.organizations.models import Domain, Organization, OrganizationProfile, OrganizationSetting


@admin.register(Organization)
class OrganizationAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ["name_en", "name_am"]
    search_fields = ["name_en", "name_am"]

    fieldsets = (
        (
            "Organization Details",
            {
                "fields": ("name_en", "name_am"),
            },
        ),
    )

    show_in_index = True


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "contact_phone",
        "contact_email",
        "postal_code",
        "address",
    ]
    search_fields = [
        "organization__name_en",
        "organization__name_am",
        "contact_phone",
        "contact_email",
        "postal_code",
    ]

    fieldsets = (
        (
            "Organization Profile Details",
            {
                "fields": (
                    "organization",
                    "description",
                    "contact_phone",
                    "contact_email",
                    "address",
                    "postal_code",
                    "logo",
                ),
            },
        ),
    )

    readonly_fields = ["logo"]

    show_in_index = True


@admin.register(OrganizationSetting)
class OrganizationSettingAdmin(admin.ModelAdmin):
    list_display = ["organization", "auto_ref_number_letters"]
    search_fields = ["organization__name_en", "organization__name_am"]
    fieldsets = (
        (
            "Settings",
            {
                "fields": (
                    "organization",
                    "auto_ref_number_letters",
                ),
            },
        ),
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["domain", "tenant"]
    search_fields = ["domain", "tenant__name_en"]

    fieldsets = (
        (
            "Domain Details",
            {
                "fields": ("domain", "tenant", "is_primary"),
            },
        ),
    )

    show_in_index = True
