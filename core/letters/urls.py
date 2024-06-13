from django.urls import path
from django.urls.resolvers import URLPattern

from core.workflows.urls import workflow_url_patterns

from .apis import DeleteLetterApi, LetterCreateApi, LetterDetailApi, LetterListApi, LetterUpdateApi

app_name = "letters"

urlpatterns: list[URLPattern] = [
    path("", LetterListApi.as_view(), name="letter-list"),
    path("<uuid:letter_id>/", LetterDetailApi.as_view(), name="letter-detail"),
    path("create/", LetterCreateApi.as_view(), name="letter-create"),
    path("<uuid:letter_id>/update/", LetterUpdateApi.as_view(), name="letter-update"),
    path("<uuid:letter_id>/delete/", DeleteLetterApi.as_view(), name="letter-delete"),
]

urlpatterns.extend(workflow_url_patterns)
