from django.contrib import admin

from .models import Member, UserPermissions, UserPreference, UserProfile, UserSetting


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
    ]


# Admin Configuration for the UserProfile Model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "member",
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
    list_display = ["member", "is_2fa_enabled"]
    fieldsets = (
        (
            "Settings",
            {
                "fields": (
                    "member",
                    "is_2fa_enabled",
                ),
            },
        ),
    )
    readonly_fields = ["is_2fa_enabled"]


# Admin Configuration for the UserPreference Model
@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ["member"]
    fieldsets = (
        (
            "Settings",
            {
                "fields": ("member",),
            },
        ),
    )
    readonly_fields = []


# Admin Configuration for the UserPermissions Model
@admin.register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ["member"]
    fieldsets = (
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    readonly_fields = []
