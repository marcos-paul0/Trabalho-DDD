from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    PLATFORM_CHOICES = [
        ("pc", "PC"),
        ("ps4", "PlayStation 4"),
        ("ps5", "PlayStation 5"),
        ("xbox-one", "Xbox One"),
        ("xbox-series", "Xbox Series X/S"),
        ("switch", "Nintendo Switch"),
        ("mobile", "Mobile"),
    ]

    GENRE_CHOICES = [
        ("action", "Ação"),
        ("adventure", "Aventura"),
        ("rpg", "RPG"),
        ("fps", "FPS"),
        ("strategy", "Estratégia"),
        ("puzzle", "Puzzle"),
        ("sports", "Esportes"),
        ("racing", "Corrida"),
        ("indie", "Indie"),
        ("horror", "Terror"),
    ]

    STATUS_CHOICES = [
        ("completed", "Completado"),
        ("playing", "Jogando"),
        ("wishlist", "Quero Jogar"),
        ("dropped", "Abandonei"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    genres = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    developer = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    release_year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    user_rating = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="wishlist")
    progress = models.IntegerField(
        default=0, help_text="Progresso em porcentagem (0-100)"
    )
    hours_played = models.IntegerField(default=0, help_text="Horas jogadas")
    completed_date = models.DateField(null=True, blank=True)
    cover_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Games"

    def __str__(self):
        return self.title
