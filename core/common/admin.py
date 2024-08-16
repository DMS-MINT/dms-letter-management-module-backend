from django.contrib import admin
from easyaudit.admin import CRUDEventAdmin, LoginEventAdmin, RequestEventAdmin
from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent

from core.departments.admin import DepartmentAdmin
from core.departments.models import Department
from core.signatures.admin import LetterSignatureAdmin
from core.signatures.models import LetterSignature

from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("city_en", "city_am", "created_at", "updated_at")
    search_fields = ["city_en", "city_am"]
    ordering = ["city_en"]
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "city_en",
                    "city_am",
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


# from core.users.admin import BaseUserParentAdmin, GuestAdmin, MemberAdmin
# from core.users.models import BaseUser, Guest, Member


class DMSAdminSite(admin.AdminSite):
    site_header = "Document Management System Admin Site"
    site_title = "DMS Admin"
    index_title = "Admin Dashboard"


dms_admin_site = DMSAdminSite(name="dms_admin")


# dms_admin_site.register(BaseUser, BaseUserParentAdmin)
# dms_admin_site.register(Guest, GuestAdmin)
# dms_admin_site.register(Member, MemberAdmin)
dms_admin_site.register(Department, DepartmentAdmin)
dms_admin_site.register(LetterSignature, LetterSignatureAdmin)
dms_admin_site.register(LoginEvent, LoginEventAdmin)
dms_admin_site.register(RequestEvent, RequestEventAdmin)
dms_admin_site.register(CRUDEvent, CRUDEventAdmin)
