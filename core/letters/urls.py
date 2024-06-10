from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    DeleteLetterApi,
    LetterApproveApi,
    LetterCreateApi,
    LetterDetailApi,
    LetterForwardApi,
    LetterListApi,
    LetterUpdateApi,
)

app_name = "letters"

urlpatterns: list[URLPattern] = [
    path("", LetterListApi.as_view(), name="letter-list"),
    path("<uuid:letter_id>/", LetterDetailApi.as_view(), name="letter-detail"),
    path("create/", LetterCreateApi.as_view(), name="letter-create"),
    path("<uuid:letter_id>/update/", LetterUpdateApi.as_view(), name="letter-update"),
    path("<uuid:letter_id>/delete/", DeleteLetterApi.as_view(), name="letter-delete"),
    path("<uuid:letter_id>/forward/", LetterForwardApi.as_view(), name="letter-forward"),
    path("<uuid:letter_id>/approve/", LetterApproveApi.as_view(), name="letter-approve"),
]
