## Clone the Repository

 - git clone https://github.com/Jizhin/task.git
 - cd talks_project

## Set Up Virtual Environment

- source env/bin/activate for linux
- source env/Scripts/activate for windows


## Social Authentication

- pip install django-allauth
- AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default Django admin login
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth specific
]
- urlpatterns = [
    ...
    path('accounts/', include('allauth.urls')),
    ...
]
- Allauth Quickstart: https://docs.allauth.org/en/latest/installation/quickstart.html
- GitHub Login: http://localhost:8000/accounts/github/login/
- Google Login: http://localhost:8000/accounts/google/login/

## Environment Variables

- GOOGLE_CLIENT_ID=""
- GOOGLE_CLIENT_SECRET=""
- SOCIAL_AUTH_GITHUB_KEY=""
- SOCIAL_AUTH_GITHUB_SECRET=""


## Test Coverage and unittest

- On pushing any change, the test suite will run automatically and provide the code coverage percentage.

## Dockerized Environment

- docker compose up --build


## WebSocket

- The Daphne server runs on port 8003.
- Live notifications: ws://localhost:8003/ws/notifications/
- Task-specific comments (replace 34 with the actual task ID): ws://localhost:8003/ws/task/34/
