from django.contrib import admin

from .models import UserPreference, UserProfile, UserSetting


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


# Admin Configuration for the UserPreference Model
@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        "user",
    ]
    search_fields = ["user__email"]
    fieldsets = (
        (
            "Settings",
            {
                "fields": ("user",),
            },
        ),
    )
    readonly_fields = []
