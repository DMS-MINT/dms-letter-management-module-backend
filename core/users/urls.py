from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import UserCreateApi, UserDeleteApi, UserDetailAPI, UserListApi, UserUpdateApi

app_name = "users"

urlpatterns: list[URLPattern] = [
    path("", UserListApi.as_view(), name="user-list"),
    path("create/", UserCreateApi.as_view(), name="user-create"),
    path("<uuid:user_id>/", UserDetailAPI.as_view(), name="user-detail"),
    path("<uuid:user_id>/update", UserUpdateApi.as_view(), name="user-update"),
    path("<uuid:user_id>/delete", UserDeleteApi.as_view(), name="user-delete"),
]
