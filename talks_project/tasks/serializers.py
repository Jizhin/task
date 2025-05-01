from rest_framework import serializers
from .models import Task, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 'assigned_users']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'task', 'content', 'timestamp']
