from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import User
from .services import user_create


# Admin Configuration for the User Model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "is_active",
        "is_staff",
        "is_admin",
        "is_superuser",
    ]
    search_fields = ["email"]
    fieldsets = (
        (
            "Authentication Info",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Permissions",
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
    readonly_fields = ["created_at", "updated_at"]

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
        else:
            try:
                user_create(**form.cleaned_data)
            except ValidationError as exc:
                self.message_user(request, str(exc), messages.ERROR)
