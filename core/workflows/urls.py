from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import LetterPublishApi, LetterRetractApi, LetterShareApi, LetterSubmitApi

workflow_url_patterns: list[URLPattern] = [
    path("<uuid:letter_id>/share/", LetterShareApi.as_view(), name="workflow-share"),
    path("<uuid:letter_id>/submit/", LetterSubmitApi.as_view(), name="letter-submit"),
    path("<uuid:letter_id>/retract/", LetterRetractApi.as_view(), name="letter-retract"),
    path("<uuid:letter_id>/publish/", LetterPublishApi.as_view(), name="letter-publish"),
]
