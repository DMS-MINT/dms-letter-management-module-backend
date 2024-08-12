from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import EnterpriseListApi

app_name = "enterprises"

urlpatterns: list[URLPattern] = [
    path("", EnterpriseListApi.as_view(), name="enterprises-list"),
]
