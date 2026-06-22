import pytest
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from rest_framework.test import APIRequestFactory, force_authenticate
from apps.movies.models import Movie
from apps.ratings.models import Rating
from apps.ratings.views import RatingViewSet


pytestmark = pytest.mark.django_db


def test_rating_model_unicidade_por_user_e_objeto():
    user = User.objects.create_user(username="u1", password="pass12345")
    movie = Movie.objects.create(
        title="M1", genres="action", release_year=2024, user=user
    )
    content_type = ContentType.objects.get_for_model(Movie)

    Rating.objects.create(
        user=user, content_type=content_type, object_id=movie.id, rating=4
    )

    with pytest.raises(IntegrityError):
        Rating.objects.create(
            user=user, content_type=content_type, object_id=movie.id, rating=3
        )


def test_rating_str_representation():
    user = User.objects.create_user(username="u1", password="pass12345")
    movie = Movie.objects.create(
        title="M1", genres="action", release_year=2024, user=user
    )
    content_type = ContentType.objects.get_for_model(Movie)
    rating = Rating.objects.create(
        user=user, content_type=content_type, object_id=movie.id, rating=5
    )
    assert str(rating) == "u1 - 5 stars"


def test_rating_viewset_create_atualiza_se_ja_existir():
    user = User.objects.create_user(username="u1", password="pass12345")
    movie = Movie.objects.create(
        title="M1", genres="action", release_year=2024, user=user
    )
    content_type = ContentType.objects.get_for_model(Movie)

    factory = APIRequestFactory()
    view = RatingViewSet.as_view({"post": "create"})

    request_1 = factory.post(
        "/api/ratings/",
        {
            "content_type": content_type.id,
            "object_id": movie.id,
            "rating": 4,
            "comment": "bom",
        },
        format="json",
    )
    force_authenticate(request_1, user=user)
    response_1 = view(request_1)

    assert response_1.status_code == 201
    assert Rating.objects.count() == 1

    request_2 = factory.post(
        "/api/ratings/",
        {
            "content_type": content_type.id,
            "object_id": movie.id,
            "rating": 2,
            "comment": "ok",
        },
        format="json",
    )
    force_authenticate(request_2, user=user)
    response_2 = view(request_2)

    assert response_2.status_code == 200
    assert Rating.objects.count() == 1
    rating = Rating.objects.get()
    assert rating.rating == 2
    assert rating.comment == "ok"
