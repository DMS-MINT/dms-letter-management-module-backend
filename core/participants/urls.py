from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import ParticipantCreateApi

app_name = "users"

urlpatterns: list[URLPattern] = [
    path("create/", ParticipantCreateApi.as_view(), name="participant-create"),
]
