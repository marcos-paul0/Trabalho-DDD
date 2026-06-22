from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class CreateGameDTO:
    user_id: int
    title: str
    platform: str
    release_year: int
    genres: str
    description: str = ""
    developer: str = ""
    publisher: str = ""
    rating: Decimal = Decimal("0")
    user_rating: Decimal | None = None
    status: str = "wishlist"
    progress: int | None = None
    hours_played: int = 0
    completed_date: date | None = None
    cover_url: str = ""


@dataclass(frozen=True)
class UpdateGameDTO:
    user_id: int
    game_id: int
    title: str
    platform: str
    release_year: int
    genres: str
    description: str = ""
    developer: str = ""
    publisher: str = ""
    rating: Decimal = Decimal("0")
    user_rating: Decimal | None = None
    status: str = "wishlist"
    progress: int | None = None
    hours_played: int = 0
    completed_date: date | None = None
    cover_url: str = ""


@dataclass(frozen=True)
class UpdateGameProgressDTO:
    user_id: int
    game_id: int
    progress: int


@dataclass(frozen=True)
class RateGameDTO:
    user_id: int
    game_id: int
    rating: Decimal


@dataclass(frozen=True)
class RegisterPlaySessionDTO:
    user_id: int
    game_id: int
    hours: int
    progress: int | None = None
