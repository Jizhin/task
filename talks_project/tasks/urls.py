from django.urls import path
from .views import TaskListCreateView, TaskDetailUpdateDeleteView, CommentCreateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view(), name='task-detail-update-delete'),

    path('tasks/<int:task_id>/comments/', CommentCreateView.as_view(), name='comment-list'),
    path('tasks/<int:task_id>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('tasks/<int:task_id>/comments/delete/<int:comment_id>/' , CommentCreateView.as_view() , name='comment-delete') ,
    # Create a new comment for a task

]