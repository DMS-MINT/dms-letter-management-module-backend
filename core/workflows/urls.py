from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    LetterCloseApi,
    LetterPublishApi,
    LetterRejectApi,
    LetterReopenApi,
    LetterRetractApi,
    LetterShareApi,
    LetterSubmitApi,
)

workflow_url_patterns: list[URLPattern] = [
    path("<uuid:id>/share/", LetterShareApi.as_view(), name="letter-share"),
    path("<uuid:id>/submit/", LetterSubmitApi.as_view(), name="letter-submit"),
    path("<uuid:id>/retract/", LetterRetractApi.as_view(), name="letter-retract"),
    path("<uuid:id>/publish/", LetterPublishApi.as_view(), name="letter-publish"),
    path("<uuid:id>/reject/", LetterRejectApi.as_view(), name="letter-reject"),
    path("<uuid:id>/close/", LetterCloseApi.as_view(), name="letter-close"),
    path("<uuid:id>/reopen/", LetterReopenApi.as_view(), name="letter-reopen"),
]
