import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.games.models import Game


pytestmark = pytest.mark.django_db


def _client_for(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_games_list_filtra_por_usuario():
    user_1 = User.objects.create_user(username="u1", password="pass12345")
    user_2 = User.objects.create_user(username="u2", password="pass12345")

    Game.objects.create(
        title="G1", genres="action", platform="pc", release_year=2024, user=user_1
    )
    Game.objects.create(
        title="G2", genres="rpg", platform="ps5", release_year=2024, user=user_2
    )

    response = _client_for(user_1).get("/api/games/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == "G1"


def test_games_search_filtra_por_titulo_ou_descricao():
    user = User.objects.create_user(username="u1", password="pass12345")

    Game.objects.create(
        title="Elden Ring",
        description="Soulslike",
        genres="rpg",
        platform="pc",
        release_year=2022,
        user=user,
    )
    Game.objects.create(
        title="Forza Horizon",
        description="Corrida arcade",
        genres="racing",
        platform="xbox-series",
        release_year=2021,
        user=user,
    )

    response = _client_for(user).get("/api/games/search/?q=souls")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Elden Ring"


def test_games_by_platform_filtra_plataforma():
    user = User.objects.create_user(username="u1", password="pass12345")

    Game.objects.create(
        title="G1", genres="action", platform="pc", release_year=2024, user=user
    )
    Game.objects.create(
        title="G2", genres="action", platform="ps5", release_year=2024, user=user
    )

    response = _client_for(user).get("/api/games/by_platform/?platform=ps5")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "G2"


def test_games_statistics_agrega_contagens_e_horas():
    user = User.objects.create_user(username="u1", password="pass12345")

    Game.objects.create(
        title="G1",
        genres="action",
        platform="pc",
        release_year=2024,
        user=user,
        status="completed",
        hours_played=10,
    )
    Game.objects.create(
        title="G2",
        genres="rpg",
        platform="ps5",
        release_year=2024,
        user=user,
        status="playing",
        hours_played=5,
    )
    Game.objects.create(
        title="G3",
        genres="rpg",
        platform="ps5",
        release_year=2024,
        user=user,
        status="wishlist",
        hours_played=0,
    )

    response = _client_for(user).get("/api/games/statistics/")
    assert response.status_code == 200
    assert response.data == {
        "total_games": 3,
        "completed": 1,
        "playing": 1,
        "wishlist": 1,
        "total_hours": 15,
    }


def test_games_create_completed_sem_avaliacao_rejeita_estado_invalido():
    user = User.objects.create_user(username="u3", password="pass12345")

    response = _client_for(user).post(
        "/api/games/",
        {
            "title": "Celeste",
            "genres": "indie",
            "platform": "switch",
            "release_year": 2018,
            "status": "completed",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "avaliação" in response.data["detail"]


def test_games_register_session_soma_horas_e_atualiza_progresso():
    user = User.objects.create_user(username="u4", password="pass12345")
    game = Game.objects.create(
        title="Hades",
        genres="indie",
        platform="pc",
        release_year=2020,
        user=user,
        status="wishlist",
    )

    response = _client_for(user).patch(
        f"/api/games/{game.id}/register_session/",
        {"hours": 3, "progress": 25},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["hours_played"] == 3
    assert response.data["progress"] == 25
    assert response.data["status"] == "playing"
