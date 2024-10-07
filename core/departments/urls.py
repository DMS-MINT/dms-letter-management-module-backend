from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    DepartmentCreateApi,
    DepartmentDeleteApi,
    DepartmentDetailApi,
    DepartmentListApi,
    DepartmentUpdateApi,
)

app_name = "departments"

urlpatterns: list[URLPattern] = [
    path("", DepartmentListApi.as_view(), name="department-list"),
    path("create/", DepartmentCreateApi.as_view(), name="department-create"),
    path("<uuid:department_id>/", DepartmentDetailApi.as_view(), name="department-details"),
    path("<uuid:department_id>/update/", DepartmentUpdateApi.as_view(), name="department-update"),
    path("<uuid:department_id>/delete/", DepartmentDeleteApi.as_view(), name="department-delete"),
]
