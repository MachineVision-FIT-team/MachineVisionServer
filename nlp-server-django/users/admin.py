from django.contrib import admin
from .models import Profile
from api.models import UserAPIKey


class ApiKeyInline(admin.TabularInline):
    model = UserAPIKey
    extra = 0
    fields = ("name", "key", "is_active")
    readonly_fields = ("key",)


class MachineInline(admin.TabularInline):
    model = Profile.machines.through
    extra = 0
    fields = ("machine", "created_at")
    readonly_fields = ("created_at",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "redis_key", "created_at", "first_api_key")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "redis_key")
    readonly_fields = ("redis_key", "created_at", "updated_at")
    inlines = [ApiKeyInline, MachineInline]

    def first_api_key(self, obj):
        # Show first active API key
        api_key = obj.api_keys.filter(is_active=True).first()
        return api_key.key if api_key else "No active key"

    first_api_key.short_description = "Active API Key"

    def get_queryset(self, request):
        # Optimize query by prefetching related API keys
        return (
            super()
            .get_queryset(request)
            .select_related("user")
            .prefetch_related("api_keys")
        )


admin.site.register(Profile, ProfileAdmin)
