from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "release_year",
        "status",
        "user_rating",
        "user",
        "created_at",
    )
    list_filter = ("status", "genres", "created_at")
    search_fields = ("title", "director")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informações Básicas", {"fields": ("title", "description", "user")}),
        (
            "Dados do Filme",
            {"fields": ("release_year", "director", "genres", "poster_url")},
        ),
        ("Avaliações", {"fields": ("rating", "user_rating", "status", "watched_date")}),
        (
            "Auditoria",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
