from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from .models import BaseUser, Department, Guest, Member
from .services import user_create


class BaseUserChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseUser


@admin.register(Guest)
class GuestAdmin(BaseUserChildAdmin):
    base_model = Guest
    list_display: list[str] = [
        "name",
        "address",
        "email",
        "phone_number",
        "postal_code",
    ]
    show_in_index = True


@admin.register(Member)
class MemberAdmin(BaseUserChildAdmin):
    base_model = Member
    list_display: list[str] = [
        "email",
        "full_name",
        "job_title",
        "department",
        "is_staff",
    ]
    search_fields: list[str] = ["email", "job_title", "department"]
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
    ]
    show_in_index = True

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        try:
            user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)


@admin.register(BaseUser)
class BaseUserParentAdmin(PolymorphicParentModelAdmin):
    base_model = BaseUser
    list_display: list[str] = [
        "id",
        "polymorphic_ctype_id",
        "created_at",
        "updated_at",
    ]
    child_models = (Guest, Member)
    list_filter = (PolymorphicChildModelFilter,)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "abbreviation"]
    ordering = ["name"]
