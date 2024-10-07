from tenant_users.tenants.utils import get_current_tenant

from .filters import BaseUserFilter
from .models import User


def user_get_users(current_user=User, filters=None):
    filters = filters or {}
    current_tenant_id = get_current_tenant().id

    qs = User.objects.prefetch_related("user_profile").filter(tenants__id=current_tenant_id).all()

    return BaseUserFilter(filters, qs).qs
