from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    JobTitleCreateApi,
    JobTitleDeleteApi,
    JobTitleDetailApi,
    JobTitleListApi,
    JobTitleUpdateApi,
)

app_name = "job_titles"

urlpatterns: list[URLPattern] = [
    path("", JobTitleListApi.as_view(), name="job_title-list"),
    path("create/", JobTitleCreateApi.as_view(), name="job_title-create"),
    path("<uuid:job_title_id>/", JobTitleDetailApi.as_view(), name="job_title-details"),
    path("<uuid:job_title_id>/update/", JobTitleUpdateApi.as_view(), name="job_title-update"),
    path("<uuid:job_title_id>/delete/", JobTitleDeleteApi.as_view(), name="job_title-delete"),
]
