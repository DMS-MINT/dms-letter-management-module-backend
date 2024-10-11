from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import TenantCreateApi, TenantDetailApi, TenantUpdateProfileApi, TenantUpdateSettingsApi

app_name = "tenants"

urlpatterns: list[URLPattern] = [
    path("create/", TenantCreateApi.as_view(), name="tenant-create"),
    path("<uuid:tenant_id>/", TenantDetailApi.as_view(), name="tenant-details"),
    path("update/<uuid:tenant_id>/", TenantUpdateProfileApi.as_view(), name="tenant-profile-update"),
    path("update/settings/<uuid:tenant_id>/", TenantUpdateSettingsApi.as_view(), name="tenant-settings-update"),
]
