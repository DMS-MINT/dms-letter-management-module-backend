from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import DepartmentListApi

app_name = "enterprises"

urlpatterns: list[URLPattern] = [
    path("", DepartmentListApi.as_view(), name="department-list"),
]
