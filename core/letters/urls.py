from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import LetterDetailApi, LetterListApi

app_name = "letter"

urlpatterns: list[URLPattern] = [
    path("", LetterListApi.as_view(), name="letter-list"),
    path("<uuid:letter_id>/", LetterDetailApi.as_view(), name="letter-detail"),
]
