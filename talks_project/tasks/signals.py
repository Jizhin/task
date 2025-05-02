from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Task, Comment
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

channel_layer = get_channel_layer()

@receiver(pre_save, sender=Task)
def pre_save_task(sender, instance, **kwargs):
    updated_status = []
    if instance.id:
        previous = Task.objects.get(id=instance.id)
        if previous.title != instance.title:
            status_ = f"title changed to {instance.title} by {instance.updated_by.username}"
            updated_status.append(status_)
        if previous.description != instance.description:
            status_ = f"description changed to {instance.description} by {instance.updated_by.username}"
            updated_status.append(status_)
        if previous.priority != instance.priority:
            status_ = f"priority changed to {instance.priority} by {instance.updated_by.username}"
            updated_status.append(status_)
        if previous.status != instance.status:
            status_ = f"status changed to {instance.status} by {instance.updated_by.username}"
            updated_status.append(status_)
        else:
            status_ = "Nothing changed"
            updated_status.append(status_)
        data = {
            "title": instance.title,
            "description": instance.description,
            "priority": instance.priority,
            "status": instance.status,
            "status_": updated_status
        }
        async_to_sync(channel_layer.group_send)(
            "live_data_live_data", {
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
            "status_": f"Created task with title: {instance.title} by {instance.created_by.username}"
        }
        async_to_sync(channel_layer.group_send)(
            "live_data_live_data", {
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

@receiver(post_save, sender=Comment)
def pre_save_comment(sender, instance, created, **kwargs):
    if created:
        status_ = f"New comment posted: {instance.content} to task {instance.task.title}"
    else:
        status_ = f"New comment updated: {instance.content} to task {instance.task.title}"
    comment_data = {
        "comment_id": instance.id,
        "content": instance.content,
        "task_id": instance.task.id,
        "status_": status_,
        "user": instance.user.username,
    }
    async_to_sync(channel_layer.group_send)(
        "live_data_live_data", {
            'type': 'send_live_data',
            'message': comment_data
        }
    )
    async_to_sync(channel_layer.group_send)(
        f"task_{instance.task.id}", {
            'type': 'send_comment_data',
            'message': comment_data
        }
    )

@receiver(post_delete, sender=Comment)
def post_delete_comment_notification(sender, instance, **kwargs):
    comment_data = {
        "comment_id": instance.id,
        "content": instance.content,
        "task_id": instance.task.id,
        "status_": f"Comment deleted for task '{instance.task.title}'",
        "user": instance.user.username,
    }
    async_to_sync(channel_layer.group_send)(
        "live_data_live_data", {
            "type": "send_live_data",
            "message": comment_data
        }
    )
    async_to_sync(channel_layer.group_send)(
        f"task_{instance.task.id}", {
            "type": "send_comment_data",
            "message": comment_data
        }
    )