from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path("auth/", include(("core.authentication.urls", "authentication"), namespace="authentication")),
    path("comments/", include(("core.comments.urls", "comments"), namespace="comments")),
    path("contacts/", include(("core.contacts.urls", "contacts"), namespace="contacts")),
    path("departments/", include(("core.departments.urls", "departments"), namespace="departments")),
    path("enterprises/", include(("core.enterprises.urls", "enterprises"), namespace="enterprises")),
    path("job_titles/", include(("core.job_titles.urls", "job_titles"), namespace="job_titles")),
    path("letters/", include(("core.letters.urls", "letters"), namespace="letters")),
    path("notifications/", include(("core.notifications.urls", "notifications"), namespace="notifications")),
    path("organizations/", include(("core.organizations.urls", "organizations"), namespace="organizations")),
    path("participants/", include(("core.participants.urls", "participants"), namespace="participants")),
    path("users/", include(("core.users.urls", "users"), namespace="users")),
    path("signatures/", include(("core.signatures.urls", "signatures"), namespace="signatures")),
]
