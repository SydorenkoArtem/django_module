from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import Cash


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Cash.objects.create(username_id=instance.id)
