from django.urls import path
from django.urls.resolvers import URLPattern

from core.workflows.urls import workflow_url_patterns

from .apis import LetterCreateApi, LetterDeleteApi, LetterDetailApi, LetterListApi, LetterUpdateApi

app_name = "letters"

urlpatterns: list[URLPattern] = [
    path("", LetterListApi.as_view(), name="letter-list"),
    path("create/", LetterCreateApi.as_view(), name="letter-create"),
    path("<slug:reference_number>/", LetterDetailApi.as_view(), name="letter-detail"),
    path("<slug:reference_number>/update/", LetterUpdateApi.as_view(), name="letter-update"),
    path("<slug:reference_number>/delete/", LetterDeleteApi.as_view(), name="letter-delete"),
]

urlpatterns.extend(workflow_url_patterns)
