from django.urls import path

from .consumers import LetterConsumer

app_name = "letters"

letter_websocket_urlpatterns = [
    path("ws/letters/<slug:reference_number>/", LetterConsumer.as_asgi(), name="letter-detail"),
]
