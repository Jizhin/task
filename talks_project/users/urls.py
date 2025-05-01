from django.urls import path
from .views import RegisterView, LoginView, GitHubTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('github/token/', GitHubTokenView.as_view(), name='github-token'),
]