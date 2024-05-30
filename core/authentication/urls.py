from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import SecureAPIView, UserJwtLoginApi, UserJwtLogoutApi, UserMeApi

app_name = "authentication"

urlpatterns: list[URLPattern] = [
    path("login/", UserJwtLoginApi.as_view(), name="auth-login"),
    path("logout/", UserJwtLogoutApi.as_view(), name="auth-logout"),
    path("me/", UserMeApi.as_view(), name="auth-me"),
    path("secure/", SecureAPIView.as_view(), name="auth-secure"),
]
