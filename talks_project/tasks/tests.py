from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Task, Comment

User = get_user_model()

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
