from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
from tenant_users.tenants.models import TenantBase


class Organization(TenantBase):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(DomainMixin):
    pass
