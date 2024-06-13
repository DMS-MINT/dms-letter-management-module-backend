from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    DeleteLetterApi,
    ForwardLetterApi,
    LetterCreateApi,
    LetterDetailApi,
    LetterListApi,
    LetterUpdateApi,
    PublishLetterApi,
    RetractLetterApi,
    ShareLetterApi,
    SubmitLetterApi,
)

app_name = "letters"

urlpatterns: list[URLPattern] = [
    path("", LetterListApi.as_view(), name="letter-list"),
    path("<uuid:letter_id>/", LetterDetailApi.as_view(), name="letter-detail"),
    path("create/", LetterCreateApi.as_view(), name="letter-create"),
    path("<uuid:letter_id>/update/", LetterUpdateApi.as_view(), name="letter-update"),
    path("<uuid:letter_id>/delete/", DeleteLetterApi.as_view(), name="letter-delete"),
    path("<uuid:letter_id>/share/", ShareLetterApi.as_view(), name="letter-share"),
    path("<uuid:letter_id>/submit/", SubmitLetterApi.as_view(), name="letter-submit"),
    path("<uuid:letter_id>/retract/", RetractLetterApi.as_view(), name="letter-retract"),
    path("<uuid:letter_id>/forward/", ForwardLetterApi.as_view(), name="letter-forward"),
    path("<uuid:letter_id>/publish/", PublishLetterApi.as_view(), name="letter-publish"),
]
