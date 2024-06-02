from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.models import User
from core.response import Response, PageResponse
from messenger.models import Chat, ChatMessage
from messenger.serializers import ChatMessageGetSerializer, ChatMessageUpdateSerializer, ChatMessageCreateSerializer, \
    ChatGetSerializer
from messenger.websockets import send_message


class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_chats = Chat.objects.filter(chatmember__user=request.user).distinct()

        page_number = request.query_params.get("pageNumber")
        per_page = request.query_params.get("pageSize")
        paginator = Paginator(user_chats, per_page)
        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)

        serializer = ChatGetSerializer(page_obj.object_list, many=True, context={'request': request})

        response = PageResponse(
            model=serializer.data,
            message="Page of chats was retrieved successfully",
            page_obj=page_obj,
            paginator=paginator
        )
        return JsonResponse(response.to_dict(), status=200)


class ChatMessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        try:
            Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            response = Response(errors="Chat was not found")
            return JsonResponse(response.to_dict(), status=400)

        messages = ChatMessage.objects.filter(chat_member__chat_id=chat_id).order_by("id")

        page_number = request.query_params.get("pageNumber")
        per_page = request.query_params.get("pageSize")
        paginator = Paginator(messages, per_page)
        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)

        serializer = ChatMessageGetSerializer(page_obj.object_list, many=True)

        response = PageResponse(
            model=serializer.data,
            message="Page of chat messages was retrieved successfully",
            page_obj=page_obj,
            paginator=paginator
        )
        return JsonResponse(response.to_dict(), status=200)


class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            User.objects.get(id=request.data["recipient_id"])
        except User.DoesNotExist:
            response = Response(errors="Message recipient was not found")
            return JsonResponse(response.to_dict(), status=400)

        serializer = ChatMessageCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            message = serializer.save()
            serializer = ChatMessageGetSerializer(message)

            send_message('message.send', serializer.data, serializer.data['chat']['chat_id'])

            response = Response(model=serializer.data, message="Message was created successfully")
            return JsonResponse(response.to_dict(), status=200)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def put(self, request, id):
        try:
            message = ChatMessage.objects.get(id=id)
        except ChatMessage.DoesNotExist:
            response = Response(errors="Message was not found")
            return JsonResponse(response.to_dict(), status=400)

        serializer = ChatMessageUpdateSerializer(message, data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            serializer = ChatMessageGetSerializer(message)

            send_message('message.update', serializer.data, serializer.data['chat']['chat_id'])

            response = Response(model=serializer.data, message="Message info was updated successfully")
            return JsonResponse(response.to_dict(), status=200)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def delete(self, request, id):
        try:
            message = ChatMessage.objects.get(id=id)
            chat_id = message.chat_member.chat_id
        except ChatMessage.DoesNotExist:
            response = Response(errors="Message was not found")
            return JsonResponse(response.to_dict(), status=400)

        message.delete()

        send_message('message.delete', id, chat_id)

        response = Response(message="Message was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)
