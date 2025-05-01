clone the repo:

git clone https://github.com/Jizhin/task.git
cd talks_project

activate env: source env/bin/activate or source env/Scripts/activate

for social authentications:
pip install django-allauth
AUTHENTICATION_BACKENDS = [
    ...
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
    ...
]

urlpatterns = [
    ...
    path('accounts/', include('allauth.urls')),
    ...
]

https://docs.allauth.org/en/latest/installation/quickstart.html

for social authentication:

pip install social-auth-app-django

documentaion: https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
for github: https://python-social-auth.readthedocs.io/en/latest/backends/github.html


dockerized environemnt:

docker compose up --build
