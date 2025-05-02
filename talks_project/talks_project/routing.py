from django.urls import path
from . import notification

websocket_urlpatterns = [
    path("ws/notifications/" , notification.NotificationConsumer.as_asgi()) ,
    path(r'ws/task/(?P<task_id>\d+)/$', notification.NotificationConsumer.as_asgi()),
]

