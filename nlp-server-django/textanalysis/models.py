from django.db import models
from django.core.validators import RegexValidator


class ObjectKeyword(models.Model):
    """Keywords representing objects that can be acted upon (e.g., 'light', 'door')"""

    keyword = models.CharField(max_length=100, unique=True)
    # Machine-readable identifier for commands (e.g., 'LIGHT_001')
    identifier = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                r"^[A-Z0-9_]+$",
                "Only uppercase letters, numbers, and underscores allowed",
            )
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["keyword"]),
        ]

    def __str__(self):
        return f"{self.keyword} ({self.identifier})"


class ActionVerb(models.Model):
    """Action verbs for commands (e.g., 'turn on', 'open')"""

    verb = models.CharField(max_length=100, unique=True)
    # Machine-readable identifier for commands (e.g., 'ACTIVATE')
    identifier = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                r"^[A-Z0-9_]+$",
                "Only uppercase letters, numbers, and underscores allowed",
            )
        ],
    )
    # Alternative phrases that mean the same thing
    related_words = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["verb"]),
        ]

    def __str__(self):
        return f"{self.verb} ({self.identifier})"
