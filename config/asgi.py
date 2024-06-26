import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from core.letters.consumers import LetterConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.base")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path(
                "ws/letters/<slug:reference_number>/",
                LetterConsumer.as_asgi(),
            ),
        ]),
    ),
})
