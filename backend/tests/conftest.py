"""
Fixtures e utilitários de teste para o projeto Media Vault.
"""

import pytest
from django.contrib.auth.models import User


@pytest.fixture
def test_user(db):
    """Cria um usuário de teste."""
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def test_user_with_profile(test_user):
    """Cria um usuário com perfil completo."""
    profile = test_user.profile
    profile.bio = "Test user bio"
    profile.favorite_genre_movies = "Action"
    profile.favorite_genre_games = "RPG"
    profile.save()
    return test_user
