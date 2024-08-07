from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path("auth/", include(("core.authentication.urls", "authentication"), namespace="authentication")),
    path("comments/", include(("core.comments.urls", "comments"), namespace="comments")),
    path("letters/", include(("core.letters.urls", "letters"), namespace="letters")),
    path("users/", include(("core.users.urls", "users"), namespace="users")),
    path("signatures/", include(("core.signatures.urls", "signatures"), namespace="signatures")),
]
