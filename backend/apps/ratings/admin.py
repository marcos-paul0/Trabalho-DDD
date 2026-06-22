from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "content_type", "created_at")
    list_filter = ("rating", "created_at", "content_type")
    search_fields = ("user__username", "comment")
    readonly_fields = ("created_at", "updated_at")
