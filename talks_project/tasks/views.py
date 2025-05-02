from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskListCreateView(APIView):

    def get(self , request):
        tasks = Task.objects.all()
        task_data = []
        for task in tasks:
            task_data.append({
                'id': task.id ,
                'title': task.title ,
                'description': task.description ,
                'priority': task.priority ,
                'status': task.status ,
                'assigned_users': [user.username for user in task.assigned_users.all()] ,
                'created_by': task.created_by.username if task.created_by else None
            })

        return Response(task_data)

    def post(self , request):
        title = request.data.get('title')
        description = request.data.get('description')
        priority = request.data.get('priority')
        task_status = request.data.get('status')
        assigned_user_ids = request.data.get('assigned_users')
        if not title or not description or not priority or not task_status:
            return Response({"detail": "please provide all fields"} , status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(assigned_user_ids , list) or not assigned_user_ids:
            assigned_user = [request.user.id]
        else:
            assigned_user = assigned_user_ids
        task = Task.objects.create(
            title=title ,
            description=description ,
            priority=priority ,
            status=task_status ,
            created_by=request.user
        )
        users = User.objects.filter(id__in=assigned_user)
        task.assigned_users.set(users)
        task.save()

        return Response({
            'id': task.id ,
            'title': task.title ,
            'description': task.description ,
            'priority': task.priority ,
            'status': task.status ,
            'assigned_users': [user.username for user in task.assigned_users.all()]
        } , status=status.HTTP_201_CREATED)


class TaskDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk, assigned_users=self.request.user)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk)
        if task:
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'status': task.status,
                'assigned_users': [user.username for user in task.assigned_users.all()],
            }
            return Response(task_data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        task = self.get_object(pk)
        if task:
            title = request.data.get('title', task.title)
            description = request.data.get('description', task.description)
            priority = request.data.get('priority', task.priority)
            task_status = request.data.get('status', task.status)

            task.title = title
            task.description = description
            task.priority = priority
            task.status = task_status
            task.updated_by = request.user
            task.save()
            new_user_ids =  request.data.get('assigned_users')
            if new_user_ids:
                existing_users = set(task.assigned_users.values_list('id' , flat=True))
                users_to_add = User.objects.filter(id__in=new_user_ids).exclude(id__in=existing_users)
                task.assigned_users.add(*users_to_add)

            return Response({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'status': task.status,
                'assigned_users': [user.username for user in task.assigned_users.all()],
            })
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        task = self.get_object(pk)
        if task:
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request , task_id):
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return Response({"detail": "Task not found."} , status=status.HTTP_404_NOT_FOUND)

        comments = task.comments.all()
        comment_data = []
        for comment in comments:
            comment_data.append({
                'id': comment.id ,
                'user': comment.user.username ,
                'content': comment.content ,
                'timestamp': comment.timestamp ,
            })

        return Response(comment_data)

    def post(self , request , task_id):
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return Response({"detail": "Task not found."} , status=status.HTTP_404_NOT_FOUND)
        content = request.data.get('content')
        if not content:
            return Response({"detail": "Comment content is required."} , status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(
            task=task ,
            user=request.user ,
            content=content ,
        )

        return Response({
            'id': comment.id ,
            'task': comment.task.id ,
            'user': comment.user.username ,
            'content': comment.content ,
            'timestamp': comment.timestamp ,
        } , status=status.HTTP_201_CREATED)

    def delete(self, request, task_id, comment_id):
        task = Task.objects.get(id=int(task_id))
        comment = Comment.objects.get(id=int(comment_id) , task=task)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
