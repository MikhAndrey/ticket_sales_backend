from django.db import models

from chat.models import Chat
from user.models import User


class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    chat_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
