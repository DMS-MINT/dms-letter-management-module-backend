import json

from channels.generic.websocket import AsyncWebsocketConsumer


class LetterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.reference_number = self.scope["url_route"]["kwargs"]["reference_number"]
        self.room_group_name = f"letter_{self.reference_number}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "letter_update",
                "message": data["message"],
            },
        )

    async def letter_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
