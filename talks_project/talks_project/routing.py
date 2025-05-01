from django.urls import path
from . import notification

websocket_urlpatterns = [
    path("ws/notifications/" , notification.NotificationConsumer.as_asgi()) ,
]

