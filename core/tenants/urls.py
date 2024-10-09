from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import TenantCreateApi, TenantDetailApi

app_name = "tenants"

urlpatterns: list[URLPattern] = [
    path("create/", TenantCreateApi.as_view(), name="tenant-create"),
    path("<uuid:tenant_id>/", TenantDetailApi.as_view(), name="tenant-details"),
]
