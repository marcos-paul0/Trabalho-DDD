from __future__ import annotations

from abc import ABC, abstractmethod

from .entities import GameCatalogItem


class GameCatalogRepository(ABC):
    """Abstração de persistência para a Aggregate Root GameCatalogItem."""

    @abstractmethod
    def get_by_id(self, game_id: int, user_id: int) -> GameCatalogItem | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: int) -> list[GameCatalogItem]:
        raise NotImplementedError

    @abstractmethod
    def save(self, game: GameCatalogItem) -> GameCatalogItem:
        raise NotImplementedError

    @abstractmethod
    def delete(self, game_id: int, user_id: int) -> None:
        raise NotImplementedError
