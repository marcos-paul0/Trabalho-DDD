from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    GENRE_CHOICES = [
        ("action", "Ação"),
        ("comedy", "Comédia"),
        ("drama", "Drama"),
        ("horror", "Terror"),
        ("sci-fi", "Ficção Científica"),
        ("romance", "Romance"),
        ("thriller", "Suspense"),
        ("animation", "Animação"),
        ("documentary", "Documentário"),
        ("fantasy", "Fantasia"),
    ]

    STATUS_CHOICES = [
        ("watched", "Assistido"),
        ("watching", "Assistindo"),
        ("wishlist", "Quero Assistir"),
        ("dropped", "Abandonei"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    genres = models.CharField(max_length=100)
    release_year = models.IntegerField()
    director = models.CharField(max_length=200, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    user_rating = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="wishlist")
    watched_date = models.DateField(null=True, blank=True)
    poster_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title
