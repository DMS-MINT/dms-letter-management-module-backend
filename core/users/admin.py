from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import User
from .services import user_create


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    base_model = User
    list_display = [
        "email",
        "full_name_en",
        "full_name_am",
        "job_title",
        "department",
        "is_staff",
        "is_2fa_enabled",
    ]
    search_fields = [
        "email",
        "first_name_en",
        "middle_name_en",
        "last_name_en",
        "first_name_am",
        "middle_name_am",
        "last_name_am",
        "job_title__title_en",
        "job_title__title_am",
        "department__department_name_en",
        "department__department_name_am",
    ]

    fieldsets = (
        (
            "Authentication Info",
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Personal Info (English)",
            {
                "fields": (
                    "first_name_en",
                    "middle_name_en",
                    "last_name_en",
                    "phone_number",
                ),
            },
        ),
        (
            "Personal Info (Amharic)",
            {
                "fields": (
                    "first_name_am",
                    "middle_name_am",
                    "last_name_am",
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

    readonly_fields = [
        "last_login",
        "date_joined",
        "updated_at",
    ]

    show_in_index = True

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        try:
            user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
