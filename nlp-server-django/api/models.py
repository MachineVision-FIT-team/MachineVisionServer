from django.db import models
from machines.models import Machine
import uuid
from django.apps import apps
from typing import Type, List


class ApiKey(models.Model):
    """Abstract base class for API key authentication"""

    key = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} ({self.owner_name})"

    @property
    def owner_name(self):
        raise NotImplementedError("Subclasses must implement this property")

    @classmethod
    def get_all_subclasses(cls) -> List[Type["ApiKey"]]:
        """Get all concrete subclasses of ApiKey across all installed apps"""
        subclasses = []
        for model in apps.get_models():
            if (
                isinstance(model, type)
                and issubclass(model, cls)
                and model != cls
                and not model._meta.abstract
            ):
                subclasses.append(model)
        return subclasses

    def get_auth_object(self):
        """Return authentication object and type for validated API key"""
        raise NotImplementedError("Subclasses must implement get_auth_object()")


class UserAPIKey(ApiKey):
    """API keys for user authentication"""

    profile = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="api_keys"
    )

    class Meta:
        verbose_name = "User API Key"
        verbose_name_plural = "User API Keys"

    @property
    def owner_name(self):
        return self.profile.user.username

    def get_auth_object(self):
        return {"type": "user", "object": self.profile.user}


class MachineApiKey(ApiKey):
    """API keys for machine authentication"""

    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE, related_name="api_keys"
    )

    class Meta:
        verbose_name = "Machine API Key"
        verbose_name_plural = "Machine API Keys"

    @property
    def owner_name(self):
        return self.machine.name

    def get_auth_object(self):
        return {"type": "machine", "object": self.machine}
