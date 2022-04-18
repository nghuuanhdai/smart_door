"""
ASGI config for smart_door project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import apps.home.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_door.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.home.routing.websocket_urlpatterns
        )
    ),
})