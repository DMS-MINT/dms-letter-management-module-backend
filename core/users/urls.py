from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import UserDetailAPI, UserListApi

app_name = "users"

urlpatterns: list[URLPattern] = [
    path("", UserListApi.as_view(), name="user-list"),
    path("<uuid:user_id>/", UserDetailAPI.as_view(), name="user-detail"),
]
