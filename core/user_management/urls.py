from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import MemberCreateApi, MemberDetailApi, MemberListApi

app_name = "members"

urlpatterns: list[URLPattern] = [
    path("", MemberListApi.as_view(), name="member-list"),
    path("create/", MemberCreateApi.as_view(), name="member-create"),
    path("<uuid:member_id>/", MemberDetailApi.as_view(), name="member-detail"),
    # path("<uuid:member_id>/update", MemberUpdateApi.as_view(), name="member-update"),
    # path("<uuid:member_id>/delete", MemberDeleteApi.as_view(), name="member-delete"),
]
