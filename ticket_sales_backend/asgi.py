"""
ASGI config for ticket_sales_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from messenger.token_auth import JWTAuthMiddleware
from messenger.websockets import ChatMessageConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_sales_backend.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddleware(
        URLRouter([
            path('ws/chats/', ChatMessageConsumer.as_asgi()),
        ])
    ),
})
