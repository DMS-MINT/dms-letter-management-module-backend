from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from .models import BaseUser, Guest, Member


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
        "username",
        "full_name",
        "job_title",
        "department",
        "is_staff",
    ]
    readonly_fields: list[str] = [
        "last_login",
        "date_joined",
    ]
    show_in_index = True


@admin.register(BaseUser)
class BaseUserParentAdmin(PolymorphicParentModelAdmin):
    base_model = BaseUser
    list_display: list[str] = [
        "id",
        "polymorphic_ctype_id",
        "created",
        "modified",
    ]
    child_models = (Guest, Member)
    list_filter = (PolymorphicChildModelFilter,)
