from django.urls import re_path

from . import admin_websocket

websocket_urlpatterns = [
    re_path(r'ws/admin/(?P<room_id>\w+)/$', admin_websocket.AdminControlConsumer.as_asgi()),
]