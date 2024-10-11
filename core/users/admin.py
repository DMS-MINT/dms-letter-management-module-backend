from django.contrib import admin

from .models import User


# Admin Configuration for the User Model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "is_active",
        "is_staff",
        # "is_admin",
        "is_superuser",
    ]
    search_fields = ["email"]
    fieldsets = (
        (
            "Authentication Info",
            {
                "fields": ("email",),
            },
        ),
        (
            "Tenants",
            {
                "fields": ("tenants",),
            },
        ),
        (
            "Global Permissions",
            {
                "fields": ("is_active", "is_staff", "is_admin", "is_superuser"),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
    readonly_fields = ["email", "created_at", "updated_at", "is_admin", "is_staff", "is_superuser"]
