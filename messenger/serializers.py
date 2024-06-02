from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from core.models import User
from messenger.models import ChatMessage, ChatMember, Chat


class ChatMessageGetSerializer(serializers.ModelSerializer):
    chat = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'date', 'chat']

    def get_chat(self, obj: ChatMessage):
        return {
            "sender_id": obj.chat_member.user.id,
            "name": obj.chat_member.user.login,
            "chat_id": obj.chat_member.chat_id
        }


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    recipient_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    recipient_id.default_error_messages['does_not_exist'] = 'Recipient was not found'

    text = serializers.CharField(max_length=500)

    class Meta:
        model = ChatMessage
        fields = ['text', 'recipient_id']

    def create(self, validated_data):
        sender = self.context['request'].user
        recipient = validated_data.pop('recipient_id')
        text = validated_data.pop('text')

        chat = Chat.objects.filter(chatmember__user=sender).filter(chatmember__user=recipient).first()

        with transaction.atomic():
            if not chat:
                chat = Chat.objects.create()
                ChatMember.objects.create(chat=chat, user=sender, chat_name=recipient.login)
                ChatMember.objects.create(chat=chat, user=recipient, chat_name=sender.login)

            chat_member = ChatMember.objects.get(chat=chat, user=sender)
            message = ChatMessage.objects.create(date=timezone.now(), text=text, chat_member=chat_member)

        return message


class ChatMessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['text']
