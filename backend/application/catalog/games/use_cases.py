from __future__ import annotations

from domain.shared.exceptions import DomainException
from domain.catalog.games.factories import GameCatalogItemFactory
from domain.catalog.games.repositories import GameCatalogRepository
from domain.catalog.games.services import GameProgressService

from .dtos import (
    CreateGameDTO,
    RateGameDTO,
    RegisterPlaySessionDTO,
    UpdateGameDTO,
    UpdateGameProgressDTO,
)


class CreateGameUseCase:
    def __init__(self, repository: GameCatalogRepository):
        self.repository = repository

    def execute(self, dto: CreateGameDTO):
        game = GameCatalogItemFactory.create(**dto.__dict__)
        return self.repository.save(game)


class UpdateGameUseCase:
    def __init__(self, repository: GameCatalogRepository):
        self.repository = repository

    def execute(self, dto: UpdateGameDTO):
        current_game = self.repository.get_by_id(dto.game_id, dto.user_id)
        if current_game is None:
            raise DomainException("Jogo não encontrado para o usuário informado.")

        game = GameCatalogItemFactory.create(
            id=dto.game_id,
            user_id=dto.user_id,
            title=dto.title,
            description=dto.description,
            genres=dto.genres,
            platform=dto.platform,
            developer=dto.developer,
            publisher=dto.publisher,
            release_year=dto.release_year,
            rating=dto.rating,
            user_rating=dto.user_rating,
            status=dto.status,
            progress=dto.progress,
            hours_played=dto.hours_played,
            completed_date=dto.completed_date,
            cover_url=dto.cover_url,
        )
        return self.repository.save(game)


class UpdateGameProgressUseCase:
    def __init__(
        self,
        repository: GameCatalogRepository,
        progress_service: GameProgressService | None = None,
    ):
        self.repository = repository
        self.progress_service = progress_service or GameProgressService()

    def execute(self, dto: UpdateGameProgressDTO):
        game = self.repository.get_by_id(dto.game_id, dto.user_id)
        if game is None:
            raise DomainException("Jogo não encontrado para o usuário informado.")
        self.progress_service.update_progress(game, dto.progress)
        return self.repository.save(game)


class RateGameUseCase:
    def __init__(self, repository: GameCatalogRepository):
        self.repository = repository

    def execute(self, dto: RateGameDTO):
        game = self.repository.get_by_id(dto.game_id, dto.user_id)
        if game is None:
            raise DomainException("Jogo não encontrado para o usuário informado.")
        game.rate(dto.rating)
        return self.repository.save(game)


class RegisterPlaySessionUseCase:
    def __init__(
        self,
        repository: GameCatalogRepository,
        progress_service: GameProgressService | None = None,
    ):
        self.repository = repository
        self.progress_service = progress_service or GameProgressService()

    def execute(self, dto: RegisterPlaySessionDTO):
        game = self.repository.get_by_id(dto.game_id, dto.user_id)
        if game is None:
            raise DomainException("Jogo não encontrado para o usuário informado.")
        self.progress_service.register_play_session(game, dto.hours, dto.progress)
        return self.repository.save(game)
