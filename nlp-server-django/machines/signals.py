# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Machine
from api.models import MachineApiKey
import uuid
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Machine)
def create_machine_resources(sender, instance, created, **kwargs):
    """Auto-create API key and redis key when a new machine is created"""
    if created:
        # Generate redis key
        instance.redis_key = f"machine_{instance.name}_{uuid.uuid4().hex[:8]}"
        instance.save(update_fields=["redis_key"])

        # Create default API key
        MachineApiKey.objects.create(machine=instance, name="Default API Key")

        logger.info(f"Created resources for machine: {instance.name}")
