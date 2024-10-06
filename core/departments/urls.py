from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    DepartmentCreateApi,
    DepartmentDeleteApi,
    DepartmentDetailApi,
    DepartmentListApi,
    DepartmentUpdateApi,
    JobTitleCreateApi,
    JobTitleDeleteApi,
    JobTitleDetailApi,
    JobTitleListApi,
    JobTitleUpdateApi,
)

app_name = "departments"

urlpatterns: list[URLPattern] = [
    path("", DepartmentListApi.as_view(), name="department-list"),
    path("", JobTitleListApi.as_view(), name="job_title-list"),
    path("create/", DepartmentCreateApi.as_view(), name="department-create"),
    path("create/", JobTitleCreateApi.as_view(), name="job_title-create"),
    path("<uuid:department_id>/", DepartmentDetailApi.as_view(), name="department-details"),
    path("<uuid:job_title_id>/", JobTitleDetailApi.as_view(), name="job_title-details"),
    path("<uuid:department_id>/update", DepartmentUpdateApi.as_view(), name="department-update"),
    path("<uuid:job_title_id>/update", JobTitleUpdateApi.as_view(), name="job_title-update"),
    path("<uuid:department_id>/delete", DepartmentDeleteApi.as_view(), name="department-delete"),
    path("<uuid:job_title_id>/delete", JobTitleDeleteApi.as_view(), name="job_title-delete"),
]
