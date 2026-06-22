from __future__ import annotations

from decimal import Decimal

from apps.games.models import Game
from domain.catalog.games.entities import GameCatalogItem
from domain.catalog.games.factories import GameCatalogItemFactory
from domain.catalog.games.repositories import GameCatalogRepository


class DjangoGameCatalogRepository(GameCatalogRepository):
    """Implementação Django ORM do repositório, mantida fora do domínio."""

    def get_by_id(self, game_id: int, user_id: int) -> GameCatalogItem | None:
        try:
            model = Game.objects.get(id=game_id, user_id=user_id)
        except Game.DoesNotExist:
            return None
        return self._to_domain(model)

    def list_by_user(self, user_id: int) -> list[GameCatalogItem]:
        return [self._to_domain(model) for model in Game.objects.filter(user_id=user_id)]

    def save(self, game: GameCatalogItem) -> GameCatalogItem:
        data = self._to_model_data(game)
        if game.id is None:
            model = Game.objects.create(**data)
        else:
            model, _created = Game.objects.update_or_create(
                id=game.id,
                user_id=game.user_id,
                defaults=data,
            )
        return self._to_domain(model)

    def delete(self, game_id: int, user_id: int) -> None:
        Game.objects.filter(id=game_id, user_id=user_id).delete()

    def _to_domain(self, model: Game) -> GameCatalogItem:
        return GameCatalogItemFactory.create(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            description=model.description,
            genres=model.genres,
            platform=model.platform,
            developer=model.developer,
            publisher=model.publisher,
            release_year=model.release_year,
            rating=model.rating or Decimal("0"),
            user_rating=model.user_rating,
            status=model.status,
            progress=model.progress,
            hours_played=model.hours_played,
            completed_date=model.completed_date,
            cover_url=model.cover_url,
        )

    def _to_model_data(self, game: GameCatalogItem) -> dict:
        return {
            "user_id": game.user_id,
            "title": game.title.value,
            "description": game.description,
            "genres": game.genres,
            "platform": game.platform.value,
            "developer": game.developer,
            "publisher": game.publisher,
            "release_year": game.release_year.value,
            "rating": game.rating,
            "user_rating": game.user_rating.as_decimal(),
            "status": game.status.value,
            "progress": game.progress.value,
            "hours_played": game.hours_played.value,
            "completed_date": game.completed_date,
            "cover_url": game.cover_url,
        }
