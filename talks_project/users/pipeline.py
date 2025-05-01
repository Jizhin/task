import requests
from django.core.files.base import ContentFile

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'github':
        avatar_url = response.get('avatar_url')
        name = response.get('name')
        if name:
            user.first_name = name.split()[0]
            if len(name.split()) > 1:
                user.last_name = name.split()[1]
        if avatar_url and not user.avatar:
            r = requests.get(avatar_url)
            user.avatar.save(f'{user.username}_avatar.jpg', ContentFile(r.content), save=True)
        user.save()
