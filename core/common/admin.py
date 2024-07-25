from django.contrib import admin
from easyaudit.admin import CRUDEventAdmin, LoginEventAdmin, RequestEventAdmin
from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent

from core.signatures.admin import SignatureAdmin
from core.signatures.models import Signature
from core.users.admin import (
    BaseUserParentAdmin,
    DepartmentAdmin,
    GuestAdmin,
    MemberAdmin,
)
from core.users.models import BaseUser, Department, Guest, Member  # noqa: F811


class DMSAdminSite(admin.AdminSite):
    site_header = "Document Management System Admin Site"
    site_title = "DMS Admin"
    index_title = "Admin Dashboard"


dms_admin_site = DMSAdminSite(name="dms_admin")


dms_admin_site.register(BaseUser, BaseUserParentAdmin)
dms_admin_site.register(Guest, GuestAdmin)
dms_admin_site.register(Member, MemberAdmin)
dms_admin_site.register(Department, DepartmentAdmin)
dms_admin_site.register(Signature, SignatureAdmin)
dms_admin_site.register(LoginEvent, LoginEventAdmin)
dms_admin_site.register(RequestEvent, RequestEventAdmin)
dms_admin_site.register(CRUDEvent, CRUDEventAdmin)
