from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "full_name_en",
        "full_name_am",
        "address",
        "email",
        "phone_number",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "full_name_en",
        "full_name_am",
        "email",
        "phone_number",
        "address__city_en",
        "address__city_am",
    )
    list_filter = ("address",)
    ordering = ("full_name_en",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "full_name_en",
                    "full_name_am",
                    "email",
                    "phone_number",
                    "address",
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
        return f"{obj.address.city_en} / {obj.address.city_am}"

    address.short_description = "Address"
