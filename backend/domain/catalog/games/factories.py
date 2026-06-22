from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from domain.shared.value_objects import MediaTitle, ReleaseYear

from .entities import GameCatalogItem
from .value_objects import GameRating, GameStatus, HoursPlayed, Platform, ProgressPercentage


class GameCatalogItemFactory:
    """Factory para criar jogos em estado inicial válido dentro do domínio."""

    @staticmethod
    def create(
        *,
        user_id: int,
        title: str,
        platform: str,
        release_year: int,
        genres: str,
        description: str = "",
        developer: str = "",
        publisher: str = "",
        rating: Any = Decimal("0"),
        user_rating: Any = None,
        status: str = GameStatus.WISHLIST,
        progress: int | None = None,
        hours_played: int = 0,
        completed_date: date | None = None,
        cover_url: str = "",
        id: int | None = None,
    ) -> GameCatalogItem:
        status_vo = GameStatus(status)

        if progress is None:
            progress = 100 if status_vo.value == GameStatus.COMPLETED else 0

        if status_vo.value == GameStatus.COMPLETED and completed_date is None:
            completed_date = date.today()

        return GameCatalogItem(
            id=id,
            user_id=user_id,
            title=MediaTitle(title),
            description=description or "",
            genres=genres or "",
            platform=Platform(platform),
            developer=developer or "",
            publisher=publisher or "",
            release_year=ReleaseYear(int(release_year)),
            rating=Decimal(str(rating or 0)),
            user_rating=GameRating(user_rating),
            status=status_vo,
            progress=ProgressPercentage(int(progress)),
            hours_played=HoursPlayed(int(hours_played or 0)),
            completed_date=completed_date,
            cover_url=cover_url or "",
        )
