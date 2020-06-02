from django.urls import path

from . import consumer_handler

websocket_urlpatterns = [
    path('ws/', consumer_handler.WSHandler),
    path('ws/<room_name>/', consumer_handler.WSHandler),
]
