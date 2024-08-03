from django.urls import path
from django.urls.resolvers import URLPattern

from core.workflows.urls import workflow_url_patterns

from .apis import (
    LetterBatchPermanentlyDeleteApi,
    LetterBatchRestoreApi,
    LetterBatchTrashApi,
    LetterCreateAndPublish,
    LetterCreateAndSubmitApi,
    LetterCreateApi,
    LetterDetailApi,
    LetterListApi,
    LetterPDFApi,
    LetterPermanentlyDeleteApi,
    LetterRestoreApi,
    LetterTrashApi,
    LetterUpdateApi,
    ReportPDFView,
)

app_name = "letters"

urlpatterns: list[URLPattern] = [
    path("", LetterListApi.as_view(), name="letter-list"),
    path("report/", ReportPDFView.as_view(), name="letter-report"),
    path("create/", LetterCreateApi.as_view(), name="letter-create"),
    path("create_and_submit/", LetterCreateAndSubmitApi.as_view(), name="letter-create-and-submit"),
    path("create_and_publish/", LetterCreateAndPublish.as_view(), name="letter-create-and-publish"),
    path("<slug:reference_number>/", LetterDetailApi.as_view(), name="letter-detail"),
    path("<slug:reference_number>/pdf/", LetterPDFApi.as_view(), name="letter-pdf"),
    path("<slug:reference_number>/update/", LetterUpdateApi.as_view(), name="letter-update"),
    path("<slug:reference_number>/trash/", LetterTrashApi.as_view(), name="letter-delete"),
    path("<slug:reference_number>/restore/", LetterRestoreApi.as_view(), name="letter-restore"),
    path(
        "<slug:reference_number>/permanently_delete/",
        LetterPermanentlyDeleteApi.as_view(),
        name="letter-permanently-delete",
    ),
    path("batch/trash/", LetterBatchTrashApi.as_view(), name="letter-batch-trash"),
    path("batch/restore/", LetterBatchRestoreApi.as_view(), name="letter-batch-restore"),
    path(
        "batch/permanently_delete/",
        LetterBatchPermanentlyDeleteApi.as_view(),
        name="letter-batch-permanently-delete",
    ),
]

urlpatterns.extend(workflow_url_patterns)
