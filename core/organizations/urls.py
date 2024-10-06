from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import OrganizationCreateApi, OrganizationDetailApi, OrganizationUpdateApi

app_name = "organizations"

urlpatterns: list[URLPattern] = [
    path("create/", OrganizationCreateApi.as_view(), name="organization-create"),
    path("<uuid:organization_id>/", OrganizationDetailApi.as_view(), name="organization-details"),
    path("<uuid:organization_id>/update/", OrganizationUpdateApi.as_view(), name="organization-update"),
]
