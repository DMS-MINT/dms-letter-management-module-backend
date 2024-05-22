from django.urls import include, path

urlpatterns = [
    path("users/", include(("core.users.urls", "users"), namespace="users")),
]
