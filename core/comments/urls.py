from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import CommentCreateApi, CommentDeleteApi, CommentUpdateApi

app_name = "comments"

urlpatterns: list[URLPattern] = [
    path("<uuid:id>/create/", CommentCreateApi.as_view(), name="comment-create"),
    path("<uuid:comment_id>/update/", CommentUpdateApi.as_view(), name="comment-update"),
    path("<uuid:comment_id>/delete/", CommentDeleteApi.as_view(), name="comment-delete"),
]
