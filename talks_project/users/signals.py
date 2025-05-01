from django.dispatch import receiver
from datetime import datetime
from django.db.models.signals import post_save, pre_save
from .models import CustomUser
from rest_framework.authtoken.models import Token

@receiver(pre_save, sender=CustomUser)
def pre_save_evaluation_payment_history(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        user = CustomUser.objects.get(id=instance.id)
        token , created = Token.objects.get_or_create(user=user)
