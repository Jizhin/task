from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField(null=True, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
