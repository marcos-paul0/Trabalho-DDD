from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "platform",
        "status",
        "progress",
        "user_rating",
        "user",
        "created_at",
    )
    list_filter = ("status", "platform", "genres", "created_at")
    search_fields = ("title", "developer")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informações Básicas", {"fields": ("title", "description", "user")}),
        (
            "Dados do Jogo",
            {
                "fields": (
                    "release_year",
                    "developer",
                    "publisher",
                    "platform",
                    "genres",
                    "cover_url",
                )
            },
        ),
        (
            "Progresso e Avaliação",
            {
                "fields": (
                    "status",
                    "progress",
                    "hours_played",
                    "completed_date",
                    "rating",
                    "user_rating",
                )
            },
        ),
        (
            "Auditoria",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
