import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class LetterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.letter_reference_number = self.scope["url_route"]["kwargs"]["reference_number"]
        self.room_group_name = f"letter_{self.letter_reference_number}"

        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        logger.warning(f"text_data: {text_data}")

        await self.channel_layer.group_send(self.room_group_name, {"type": "letter_update", "message": data})

    async def letter_update(self, event):
        message = event["message"]
        logger.warning(f"Event content: {json.dumps(event, default=str, indent=4)}")

        await self.send(text_data=json.dumps(message))
