from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

    PRIORITY_CHOICES = [
        (LOW , 'Low') ,
        (MEDIUM , 'Medium') ,
        (HIGH , 'High') ,
    ]

    STATUS_CHOICES = [
        (NOT_STARTED , 'Not Started') ,
        (IN_PROGRESS , 'In Progress') ,
        (COMPLETED , 'Completed') ,
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10 , choices=PRIORITY_CHOICES , default=LOW)
    status = models.CharField(max_length=15 , choices=STATUS_CHOICES , default=NOT_STARTED)
    assigned_users = models.ManyToManyField(User , related_name="tasks")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="updated_by", null=True, blank=True)



    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task , related_name='comments' , on_delete=models.CASCADE)
    user = models.ForeignKey(User , related_name='comments' , on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"
