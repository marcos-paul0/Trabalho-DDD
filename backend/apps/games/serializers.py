from rest_framework import serializers

from domain.catalog.games.value_objects import (
    GameRating,
    GameStatus,
    HoursPlayed,
    Platform,
    ProgressPercentage,
)
from domain.shared.exceptions import DomainException
from domain.shared.value_objects import MediaTitle, ReleaseYear

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "description",
            "genres",
            "platform",
            "developer",
            "publisher",
            "release_year",
            "rating",
            "user_rating",
            "status",
            "progress",
            "hours_played",
            "completed_date",
            "cover_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        try:
            if "title" in attrs:
                MediaTitle(attrs["title"])
            if "release_year" in attrs:
                ReleaseYear(attrs["release_year"])
            if "platform" in attrs:
                Platform(attrs["platform"])
            if "status" in attrs:
                GameStatus(attrs["status"])
            if "progress" in attrs:
                ProgressPercentage(attrs["progress"])
            if "hours_played" in attrs:
                HoursPlayed(attrs["hours_played"])
            if "user_rating" in attrs:
                GameRating(attrs["user_rating"])
        except DomainException as exc:
            raise serializers.ValidationError(str(exc))
        return attrs
