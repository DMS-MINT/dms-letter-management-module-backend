from django.urls import path

from .apis import ParticipantRemoveApi

app_name = "participants"

urlpatterns = [
    path("<uuid:participant_id>/delete/", ParticipantRemoveApi.as_view(), name="participant-delete"),
]
