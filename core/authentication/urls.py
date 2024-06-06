from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import LoginApi, LogoutApi, UserMeApi

app_name = "authentication"

urlpatterns: list[URLPattern] = [
    path("login/", LoginApi.as_view(), name="auth-login"),
    path("logout/", LogoutApi.as_view(), name="auth-logout"),
    path("me/", UserMeApi.as_view(), name="auth-me"),
]
