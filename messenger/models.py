from django.db import models

from core.models import User


class Chat(models.Model):
    last_message = models.ForeignKey('ChatMessage', on_delete=models.SET_NULL, null=True, blank=True)

    def update_last_message(self, message):
        self.last_message = message
        self.save()


class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    chat_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ChatMessage(models.Model):
    chat_member = models.ForeignKey(ChatMember, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.chat_member.chat.update_last_message(self)

    def delete(self, *args, **kwargs):
        chat = self.chat_member.chat
        super().delete(*args, **kwargs)
        last_message = ChatMessage.objects.filter(chat_member__chat=chat).order_by('-id').first()
        chat.update_last_message(last_message)
