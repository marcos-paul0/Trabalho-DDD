import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.movies.models import Movie


pytestmark = pytest.mark.django_db


def _client_for(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_movies_list_filtra_por_usuario():
    user_1 = User.objects.create_user(username="u1", password="pass12345")
    user_2 = User.objects.create_user(username="u2", password="pass12345")

    Movie.objects.create(title="M1", genres="action", release_year=2024, user=user_1)
    Movie.objects.create(title="M2", genres="drama", release_year=2024, user=user_2)

    response = _client_for(user_1).get("/api/movies/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == "M1"


def test_movies_search_filtra_por_titulo_ou_descricao():
    user = User.objects.create_user(username="u1", password="pass12345")

    Movie.objects.create(
        title="Inception",
        description="Dream heist",
        genres="sci-fi",
        release_year=2010,
        user=user,
    )
    Movie.objects.create(
        title="The Godfather",
        description="Mafia",
        genres="drama",
        release_year=1972,
        user=user,
    )

    response = _client_for(user).get("/api/movies/search/?q=dream")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Inception"


def test_movies_by_status_filtra_status():
    user = User.objects.create_user(username="u1", password="pass12345")

    Movie.objects.create(
        title="M1", genres="action", release_year=2024, user=user, status="watched"
    )
    Movie.objects.create(
        title="M2", genres="action", release_year=2024, user=user, status="wishlist"
    )

    response = _client_for(user).get("/api/movies/by_status/?status=watched")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "M1"


def test_movies_statistics_agrega_contagens():
    user = User.objects.create_user(username="u1", password="pass12345")

    Movie.objects.create(
        title="M1", genres="action", release_year=2024, user=user, status="watched"
    )
    Movie.objects.create(
        title="M2", genres="action", release_year=2024, user=user, status="watching"
    )
    Movie.objects.create(
        title="M3", genres="action", release_year=2024, user=user, status="wishlist"
    )

    response = _client_for(user).get("/api/movies/statistics/")
    assert response.status_code == 200
    assert response.data == {
        "total_movies": 3,
        "watched": 1,
        "watching": 1,
        "wishlist": 1,
    }
