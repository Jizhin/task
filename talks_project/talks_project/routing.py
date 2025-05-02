from django.urls import path
from . import notification

websocket_urlpatterns = [
    path("ws/notifications/" , notification.NotificationConsumer.as_asgi()) ,
    path("ws/task/<int:task_id>/" , notification.NotificationConsumer.as_asgi()) ,
]

