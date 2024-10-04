from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from core.users.models import User, UserProfile, UserSetting

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


# Admin Configuration for the UserProfile Model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "full_name_en",
        "job_title",
        "department",
        "phone_number",
    ]
    search_fields = [
        "first_name_en",
        "middle_name_en",
        "last_name_en",
        "first_name_am",
        "middle_name_am",
        "last_name_am",
        "phone_number",
        "job_title__title_en",
        "department__department_name_en",
    ]
    fieldsets = (
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
    )


# Admin Configuration for the UserSetting Model
@admin.register(UserSetting)
class UserSettingAdmin(admin.ModelAdmin):
    list_display = ["user", "is_2fa_enabled"]
    search_fields = ["user__email"]
    fieldsets = (
        (
            "Settings",
            {
                "fields": (
                    "user",
                    "is_2fa_enabled",
                ),
            },
        ),
    )
    readonly_fields = ["is_2fa_enabled"]
