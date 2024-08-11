from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import User
from .services import user_create


@admin.register(User)
class MemberAdmin(admin.ModelAdmin):
    base_model = User
    list_display: list[str] = [
        "email",
        "full_name",
        "job_title",
        "department",
        "is_staff",
        "is_2fa_enabled",
    ]
    search_fields: list[str] = ["email", "job_title", "department"]
    fieldsets = (
        (
            "Authentication Info",
            {
                "fields": (
                    "email",
                    "password",
                    "otp_secret",
                ),
            },
        ),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                ),
            },
        ),
        (
            "Job Details",
            {
                "fields": (
                    "job_title",
                    "department",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_2fa_enabled",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "updated_at",
                ),
            },
        ),
    )

    readonly_fields: list[str] = [
        "last_login",
        "date_joined",
        "updated_at",
        "otp_secret",
    ]
    show_in_index = True

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        try:
            user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
