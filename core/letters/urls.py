from django.urls import path
from django.urls.resolvers import URLPattern

from core.letters.apis.bulk_apis import LetterBulkDeleteApi, LetterBulkRestoreApi, LetterBulkTrashApi
from core.letters.apis.create_apis import LetterCreateAndPublish, LetterCreateAndSubmitApi, LetterCreateApi
from core.letters.apis.delete_apis import LetterDeleteApi, LetterRestoreApi, LetterTrashApi
from core.letters.apis.read_apis import LetterDetailApi, LetterListApi, LetterPdfView
from core.letters.apis.update_apis import LetterUpdateApi
from core.workflows.urls import workflow_url_patterns

app_name = "letters"

urlpatterns: list[URLPattern] = [
    path("", LetterListApi.as_view(), name="letter-list"),
    path("create/", LetterCreateApi.as_view(), name="letter-create"),
    path("create_and_submit/", LetterCreateAndSubmitApi.as_view(), name="letter-create-and-submit"),
    path("create_and_publish/", LetterCreateAndPublish.as_view(), name="letter-create-and-publish"),
    path("bulk/trash/", LetterBulkTrashApi.as_view(), name="letter-bulk-trash"),
    path("bulk/restore/", LetterBulkRestoreApi.as_view(), name="letter-bulk-restore"),
    path("bulk/delete/", LetterBulkDeleteApi.as_view(), name="letter-bulk-delete"),
    path("<slug:reference_number>/", LetterDetailApi.as_view(), name="letter-detail"),
    path("<slug:reference_number>/pdf/", LetterPdfView.as_view(), name="letter-pdf"),
    path("<slug:reference_number>/update/", LetterUpdateApi.as_view(), name="letter-update"),
    path("<slug:reference_number>/trash/", LetterTrashApi.as_view(), name="letter-delete"),
    path("<slug:reference_number>/restore/", LetterRestoreApi.as_view(), name="letter-restore"),
    path("<slug:reference_number>/delete/", LetterDeleteApi.as_view(), name="letter-delete"),
]

urlpatterns.extend(workflow_url_patterns)
