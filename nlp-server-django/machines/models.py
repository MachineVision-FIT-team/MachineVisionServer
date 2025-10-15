# models.py
from django.db import models
import uuid


class Machine(models.Model):
    name = models.CharField(max_length=255)
    machine_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    # Redis key for caching/sessions, indexed for lookup performance
    redis_key = models.CharField(
        max_length=400, blank=True, editable=False, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
