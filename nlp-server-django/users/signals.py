from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from api.models import UserAPIKey
import uuid
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile and API key when a new user is created"""
    if created:
        # Create profile
        profile = Profile.objects.create(user=instance)

        # Generate redis key
        profile.redis_key = f"{instance.username}_{uuid.uuid4().hex}"
        profile.save(update_fields=["redis_key"])

        # Create default API key
        UserAPIKey.objects.create(profile=profile, name=f"Default API Key")

        logger.info(f"Created profile and API key for user: {instance.username}")
