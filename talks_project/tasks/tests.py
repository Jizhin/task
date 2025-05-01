from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Task, Comment
from channels.testing import WebsocketCommunicator
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from talks_project.talks_project.notification import NotificationConsumer

User = get_user_model()

class RealTimeTaskUpdateTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user3@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user4@example.com')
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            priority=Task.HIGH,
            status=Task.NOT_STARTED
        )
        self.task.assigned_users.add(self.user1)

    async def connect_to_websocket(self, user, task_id=None):
        communicator = WebsocketCommunicator(NotificationConsumer.as_asgi(), f"/ws/notifications/?task_id={task_id}" if task_id else "/ws/notifications/")
        await communicator.connect()
        return communicator

    async def test_real_time_task_update(self):
        communicator_user1 = await self.connect_to_websocket(user=self.user1, task_id=self.task.id)
        communicator_user2 = await self.connect_to_websocket(user=self.user2, task_id=self.task.id)
        self.task.title = "Updated Test Task"
        self.task.save()
        response_user2 = await communicator_user2.receive_json_from()
        self.assertEqual(response_user2['message']['title'], "Updated Test Task")
        await communicator_user1.disconnect()
        await communicator_user2.disconnect()

    async def test_real_time_comment_addition(self):
        communicator_user1 = await self.connect_to_websocket(user=self.user1, task_id=self.task.id)
        communicator_user2 = await self.connect_to_websocket(user=self.user2, task_id=self.task.id)
        comment = Comment.objects.create(task=self.task, user=self.user1, content="This is a test comment")
        response_user2 = await communicator_user2.receive_json_from()
        self.assertEqual(response_user2['message']['comment'], "This is a test comment")
        await communicator_user1.disconnect()
        await communicator_user2.disconnect()
class TaskTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user3@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user4@example.com')

    def test_task_creation(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            priority=Task.HIGH,
            status=Task.NOT_STARTED
        )
        task.save()
        task.assigned_users.add(self.user1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.assigned_users.count(), 1)
        self.assertIn(self.user1, task.assigned_users.all())

    def test_task_update(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            priority=Task.HIGH,
            status=Task.NOT_STARTED
        )
        task.assigned_users.add(self.user1)
        task.title = "Updated Task Title"
        task.status = Task.IN_PROGRESS
        task.save()
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Task Title")
        self.assertEqual(task.status, Task.IN_PROGRESS)

    def test_task_deletion(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            priority=Task.HIGH,
            status=Task.NOT_STARTED
        )
        task.assigned_users.add(self.user1)

        task_id = task.id
        task.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)


class CommentTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user5@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user6@example.com')

        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            priority=Task.HIGH,
            status=Task.NOT_STARTED
        )
        self.task.assigned_users.add(self.user1)

    def test_comment_creation(self):
        comment = Comment.objects.create(
            task=self.task,
            user=self.user1,
            content="This is a comment."
        )

        self.assertEqual(comment.task, self.task)
        self.assertEqual(comment.user, self.user1)
        self.assertEqual(comment.content, "This is a comment.")

    def test_comment_retrieval(self):
        comment = Comment.objects.create(
            task=self.task,
            user=self.user1,
            content="This is a comment."
        )
        comments = self.task.comments.all()
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments.first().content, "This is a comment.")

    def test_comment_deletion(self):
        comment = Comment.objects.create(
            task=self.task,
            user=self.user1,
            content="This is a comment."
        )
        comment_id = comment.id
        comment.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)
