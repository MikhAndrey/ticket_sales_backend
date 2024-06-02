import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from messenger.models import Chat


class ChatMessageConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_ids = []

    async def connect(self):
        self.chat_ids = await get_chat_ids(self.scope['user'].id)

        for chat_id in self.chat_ids:
            await self.channel_layer.group_add(get_chat_key(chat_id), self.channel_name)
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
        for chat_id in self.chat_ids:
            await self.channel_layer.group_discard(get_chat_key(chat_id), self.channel_name)
        await super().disconnect(close_code)


@database_sync_to_async
def get_chat_ids(user_id):
    return list(Chat.objects.filter(chatmember__user_id=user_id).values_list('id', flat=True))


def send_message(message_type, data, chat_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        get_chat_key(chat_id),
        {
            'type': message_type,
            'data': data
        }
    )


def get_chat_key(chat_id):
    return f'chats_{chat_id}'
