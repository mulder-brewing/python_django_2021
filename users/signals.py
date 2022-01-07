from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    user = instance.user
    user.delete()

# old way to hook up signal, can use the @receiver decorator
# post_save.connect(profile_updated, sender=Profile)
# post_delete.connect(profile_deleted, sender=Profile)
