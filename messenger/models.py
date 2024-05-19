from django.db import models

from core.models import User


class Chat(models.Model):
    pass


class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    chat_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ChatMessage(models.Model):
    chat_member = models.ForeignKey(ChatMember, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date = models.DateTimeField()
