from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    ContactBulkDeleteApi,
    ContactCreateApi,
    ContactDeleteApi,
    ContactDetailApi,
    ContactListApi,
    ContactUpdateApi,
)

app_name = "contacts"

urlpatterns: list[URLPattern] = [
    path("", ContactListApi.as_view(), name="contact-list"),
    path("create/", ContactCreateApi.as_view(), name="contact-create"),
    path("<uuid:contact_id>/", ContactDetailApi.as_view(), name="contact-details"),
    path("<uuid:contact_id>/update/", ContactUpdateApi.as_view(), name="contact-update"),
    path("<uuid:contact_id>/delete/", ContactDeleteApi.as_view(), name="contact-delete"),
    path("bulk/delete/", ContactBulkDeleteApi.as_view(), name="contact-bulk-delete"),
]
