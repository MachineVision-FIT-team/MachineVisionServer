from django.db import models
from django.contrib.auth.models import User
from machines.models import Machine


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # API authentication key, indexed for lookup performance
    redis_key = models.CharField(
        max_length=256, unique=True, blank=True, null=True, db_index=True
    )
    machines = models.ManyToManyField(
        Machine, through="ProfileMachine", related_name="profiles"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ProfileMachine(models.Model):
    """Links profiles to machines with creation tracking"""

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile_machines"
    )
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE, related_name="profile_machines"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate profile-machine pairs
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "machine"], name="unique_profile_machine"
            )
        ]

    def __str__(self):
        return f"{self.profile.user.username} - {self.machine}"
