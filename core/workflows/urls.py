from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import LetterPublishApi, LetterRetractApi, LetterShareApi, LetterSubmitApi

workflow_url_patterns: list[URLPattern] = [
    path("<slug:reference_number>/share/", LetterShareApi.as_view(), name="letter-share"),
    path("<slug:reference_number>/submit/", LetterSubmitApi.as_view(), name="letter-submit"),
    path("<slug:reference_number>/retract/", LetterRetractApi.as_view(), name="letter-retract"),
    path("<slug:reference_number>/publish/", LetterPublishApi.as_view(), name="letter-publish"),
]
