from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path("letters/", include(("core.letters.urls", "letters"), namespace="letters")),
    path("users/", include(("core.users.urls", "users"), namespace="users")),
]
