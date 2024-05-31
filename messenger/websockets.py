import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class ChatMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('chat_messages', self.channel_name)
        await super().connect()

    async def message_send(self, text_data=None):
        await self.send_json(text_data)

    async def message_update(self, text_data=None):
        await self.send_json(text_data)

    async def message_delete(self, text_data=None):
        await self.send_json(text_data)

    async def send_json(self, text_data=None):
        await self.send(json.dumps(text_data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('chat_messages', self.channel_name)
        await super().disconnect(close_code)


def send_message(message_type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_messages',
        {
            'type': message_type,
            'data': data
        }
    )
