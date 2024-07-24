from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import GetDefaultSignature

app_name = "signatures"

urlpatterns: list[URLPattern] = [
    path("retrieve-signature/", GetDefaultSignature.as_view(), name="signatures-retrieve-signature"),
]
