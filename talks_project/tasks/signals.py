from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Task, Comment
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

channel_layer = get_channel_layer()

@receiver(pre_save, sender=Task)
def pre_save_task(sender, instance, **kwargs):
    if instance.id:
        previous = Task.objects.get(id=instance.id)
        if previous.title != instance.title:
            status_ = f"title changed to {instance.title}"
        elif previous.description != instance.description:
            status_ = f"description changed to {instance.description}"
        elif previous.priority != instance.priority:
            status_ = f"priority changed to {instance.priority}"
        elif previous.status != instance.status:
            status_ = f"status changed to {instance.status}"
        else:
            status_ = "Nothing changed"
        data = {
            "title": instance.title,
            "description": instance.description,
            "priority": instance.priority,
            "status": instance.status,
            "status_": status_
        }
        async_to_sync(channel_layer.group_send)(
            "live_data_live_data", {
                'type': 'send_live_data',
                'message': data
            }
        )
        async_to_sync(channel_layer.group_send)(
            f"task_{instance.id}", {
                'type': 'send_live_data',
                'message': data
            }
        )
    else:
        data = {
            "title": instance.title,
            "description": instance.description,
            "priority": instance.priority,
            "status": instance.status,
            "status_": f"Created task with title: {instance.title}"
        }
        async_to_sync(channel_layer.group_send)(
            "live_data_live_data", {
                'type': 'send_live_data',
                'message': data
            }
        )
        async_to_sync(channel_layer.group_send)(
            f"task_{instance.id}", {
                'type': 'send_live_data',
                'message': data
            }
        )

@receiver(post_delete, sender=Task)
def post_delete_task_notification(sender, instance, **kwargs):
    data = {
        "title": instance.title,
        "description": instance.description,
        "priority": instance.priority,
        "status": instance.status,
        "status_": f"Deleted task: {instance.title}"
    }
    async_to_sync(channel_layer.group_send)(
        "live_data_live_data", {
            "type": "send_live_data",
            "message": data
        }
    )
    async_to_sync(channel_layer.group_send)(
        f"task_{instance.id}", {
            "type": "send_live_data",
            "message": data
        }
    )

@receiver(pre_save, sender=Comment)
def pre_save_comment(sender, instance, **kwargs):
    if instance.id:
        previous = Comment.objects.get(id=instance.id)
    else:
        data = {
            "comment": instance.content,
            "status_": f"{instance.user.username} added a comment on {instance.task.title}"
        }
        async_to_sync(channel_layer.group_send)(
            "live_data_live_data", {
                'type': 'send_live_data',
                'message': data
            }
        )
        async_to_sync(channel_layer.group_send)(
            f"task_{instance.task.id}", {
                'type': 'send_live_data',
                'message': data
            }
        )

@receiver(post_delete, sender=Comment)
def post_delete_comment_notification(sender, instance, **kwargs):
    data = {
        "comment": instance.content,
        "status_": f"Comment deleted for task '{instance.task.title}'"
    }
    async_to_sync(channel_layer.group_send)(
        "live_data_live_data", {
            "type": "send_live_data",
            "message": data
        }
    )
    async_to_sync(channel_layer.group_send)(
        f"task_{instance.task.id}", {
            "type": "send_live_data",
            "message": data
        }
    )
