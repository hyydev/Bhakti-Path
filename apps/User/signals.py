from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a user profile when a new user is created.
    """
    if created:
        UserProfile.objects.create(user=instance)

    
