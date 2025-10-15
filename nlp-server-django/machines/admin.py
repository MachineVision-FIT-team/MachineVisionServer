# admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Machine
from api.models import MachineApiKey


class MachineApiKeyInline(admin.TabularInline):
    model = MachineApiKey
    extra = 0
    fields = ("name", "key", "is_active", "created_at")
    readonly_fields = ("key", "created_at")

    def has_add_permission(self, request, obj=None):
        # Only allow adding API keys when editing existing machine
        return obj is not None


class MachineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "machine_id",
        "redis_key_display",
        "created_at",
        "user_count",
    )
    list_filter = ("created_at",)
    search_fields = ("name", "machine_id", "redis_key")
    readonly_fields = ("redis_key_display", "created_at", "updated_at", "user_list")
    inlines = [MachineApiKeyInline]

    def redis_key_display(self, obj):
        """Show placeholder if redis_key is empty"""
        return obj.redis_key or "Generated upon save"

    redis_key_display.short_description = "Redis Key"

    def get_inline_instances(self, request, obj=None):
        # Don't show API key inline when creating new machine
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    def user_count(self, obj):
        """Show count of connected users"""
        return obj.profiles.count()

    user_count.short_description = "Connected Users"

    def user_list(self, obj):
        """Show clickable links to connected user profiles"""
        profiles = obj.profiles.select_related("user")

        if not profiles.exists():
            return "No users connected"

        links = [
            format_html(
                '<a href="{}">{}</a>',
                reverse("admin:users_profile_change", args=[profile.id]),
                profile.user.username,
            )
            for profile in profiles
        ]

        return format_html("<br/>".join(links))

    user_list.short_description = "Connected Users"

    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).prefetch_related("profiles__user")


admin.site.register(Machine, MachineAdmin)
