from django.contrib import admin
from .models import ObjectKeyword, ActionVerb


@admin.register(ObjectKeyword)
class ObjectKeywordAdmin(admin.ModelAdmin):
    list_display = ("keyword", "identifier", "created_at")
    list_filter = ("created_at",)
    search_fields = ("keyword", "identifier")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ActionVerb)
class ActionVerbAdmin(admin.ModelAdmin):
    list_display = ("verb", "identifier", "display_related_words", "created_at")
    list_filter = ("created_at",)
    search_fields = ("verb", "identifier")
    readonly_fields = ("created_at", "updated_at")

    def display_related_words(self, obj):
        """Show related words as comma-separated list"""
        if not obj.related_words:
            return "None"
        return ", ".join(obj.related_words)

    display_related_words.short_description = "Related Words"
