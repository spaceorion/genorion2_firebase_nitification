import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
# from . import consumers
from myapp.consumers import *
from django.core.asgi import get_asgi_application

from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator


from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path('ws/chating/', ChatConsumer.as_asgi()), # Using asgi
                ]
            )
            
        )
    )})