from django.db import models

from chat_member.models import ChatMember


class ChatMessage(models.Model):
    chat_member = models.ForeignKey(ChatMember, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date = models.DateTimeField()
