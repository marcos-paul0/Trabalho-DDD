import pytest
from django.contrib.auth.models import User
from apps.movies.models import Movie


@pytest.mark.django_db
class TestMovieModel:
    def test_create_movie(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        movie = Movie.objects.create(
            title="Test Movie",
            release_year=2024,
            genres="Action",
            user=user,
            status="watched",
        )
        assert movie.title == "Test Movie"
        assert movie.user == user

    def test_movie_str_representation(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        movie = Movie.objects.create(
            title="Another Movie", release_year=2024, genres="Drama", user=user
        )
        assert str(movie) == "Another Movie"
