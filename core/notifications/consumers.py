import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.sessions.models import Session

from core.users.models.user import User


@database_sync_to_async
def get_user(session_key):
    try:
        session = Session.objects.get(session_key=session_key)
        user_id = session.get_decoded().get("_auth_user_id")
        return User.objects.get(id=user_id)
    except (Session.DoesNotExist, User.DoesNotExist):
        return None


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        session_id = self.scope["query_string"].decode("utf-8").split("=")[1]

        self.user = await get_user(session_id)

        if not self.user or not self.user.is_authenticated:
            await self.close(code=4000)
            return

        self.room_group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "message": data["message"],
            },
        )

    async def send_notification(self, event):
        await self.send_json({"message": event["message"]})
