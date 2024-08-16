from django.contrib import admin

from .models import Enterprise


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = (
        "name_en",
        "name_am",
        "email",
        "phone_number",
        "address",
        "postal_code",
        "logo",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name_en",
        "name_am",
        "email",
        "phone_number",
        "address__city_en",
        "address__city_am",
    )
    list_filter = ("address", "postal_code")
    ordering = ("name_en",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name_en",
                    "name_am",
                    "email",
                    "phone_number",
                    "address",
                    "postal_code",
                    "logo",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def address(self, obj):
        return f"{obj.address.city_en} / {obj.address.city_am}" if obj.address else "N/A"

    address.short_description = "Address"
