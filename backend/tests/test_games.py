import pytest
from django.contrib.auth.models import User
from apps.games.models import Game


@pytest.mark.django_db
class TestGameModel:
    def test_create_game(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        game = Game.objects.create(
            title="Test Game",
            platform="pc",
            genres="action",
            developer="Test Dev",
            release_year=2024,
            user=user,
            status="playing",
        )
        assert game.title == "Test Game"
        assert game.user == user

    def test_game_progress(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        game = Game.objects.create(
            title="Test Game",
            platform="ps5",
            genres="RPG",
            developer="Test Dev",
            release_year=2024,
            user=user,
            progress=50,
            hours_played=20,
        )
        assert game.progress == 50
        assert game.hours_played == 20
