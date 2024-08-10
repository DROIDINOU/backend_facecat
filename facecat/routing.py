# facecat/routing.py
from django.urls import re_path
from django.urls import path
from cat.consumers import ChatConsumer  # Assurez-vous que le chemin est correct

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),

]

