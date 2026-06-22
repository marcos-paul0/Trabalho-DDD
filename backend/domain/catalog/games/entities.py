from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any

from domain.shared.exceptions import DomainException
from domain.shared.value_objects import MediaTitle, ReleaseYear

from .value_objects import (
    GameRating,
    GameStatus,
    HoursPlayed,
    Platform,
    ProgressPercentage,
)


@dataclass
class GameCatalogItem:
    """Aggregate Root que controla o ciclo de vida de um jogo no catálogo pessoal.

    O Aggregate protege as invariantes do item de catálogo. Alterações externas
    devem passar pelos comportamentos da raiz, e não pela troca direta de campos.
    """

    id: int | None
    user_id: int
    title: MediaTitle
    description: str
    genres: str
    platform: Platform
    developer: str
    publisher: str
    release_year: ReleaseYear
    rating: Decimal
    user_rating: GameRating
    status: GameStatus
    progress: ProgressPercentage
    hours_played: HoursPlayed
    completed_date: date | None
    cover_url: str

    def __post_init__(self):
        self._ensure_consistency()

    def start_playing(self) -> None:
        """Move o jogo para jogando quando ele ainda não foi concluído."""
        if self.status.value == GameStatus.COMPLETED:
            raise DomainException(
                "Um jogo completado deve ser reaberto antes de voltar para jogando."
            )
        self.status = GameStatus(GameStatus.PLAYING)
        self.completed_date = None
        self._ensure_consistency()

    def move_to_wishlist(self) -> None:
        """Retorna o jogo para wishlist somente quando ainda não existe consumo."""
        if self.hours_played.value > 0 or self.progress.value > 0:
            raise DomainException(
                "Um jogo com progresso ou horas jogadas não pode voltar para wishlist."
            )
        self.status = GameStatus(GameStatus.WISHLIST)
        self.completed_date = None
        self._ensure_consistency()

    def update_progress(self, progress: int) -> None:
        """Atualiza o progresso preservando as transições válidas de status."""
        new_progress = ProgressPercentage(progress)
        if self.status.value == GameStatus.DROPPED:
            raise DomainException(
                "Um jogo abandonado deve ser retomado antes de receber progresso."
            )
        if new_progress.value == 100:
            self.complete()
            return
        if self.status.value == GameStatus.WISHLIST and new_progress.value > 0:
            self.status = GameStatus(GameStatus.PLAYING)
        elif self.status.value == GameStatus.COMPLETED:
            self.status = GameStatus(GameStatus.PLAYING)
            self.completed_date = None
        self.progress = new_progress
        self._ensure_consistency()

    def add_played_hours(self, hours: int) -> None:
        """Soma horas jogadas e inicia o jogo quando ele sai da wishlist."""
        hours_to_add = HoursPlayed(hours)
        if hours_to_add.value == 0:
            return
        if self.status.value == GameStatus.DROPPED:
            raise DomainException(
                "Um jogo abandonado deve ser retomado antes de receber horas jogadas."
            )
        if self.status.value == GameStatus.WISHLIST:
            self.status = GameStatus(GameStatus.PLAYING)
        self.hours_played = self.hours_played.add(hours_to_add)
        self._ensure_consistency()

    def complete(self, completed_date: date | None = None) -> None:
        """Marca o jogo como concluído.

        A conclusão exige avaliação pessoal, pois a linguagem do domínio trata a
        nota como parte do fechamento da experiência do usuário com a mídia.
        """
        if self.user_rating.value is None:
            raise DomainException(
                "Não é permitido concluir um jogo sem atribuir uma avaliação pessoal."
            )
        self.progress = ProgressPercentage(100)
        self.status = GameStatus(GameStatus.COMPLETED)
        self.completed_date = completed_date or date.today()
        self._ensure_consistency()

    def drop(self) -> None:
        """Marca o jogo como abandonado quando ele ainda não foi concluído."""
        if self.status.value == GameStatus.COMPLETED:
            raise DomainException(
                "Um jogo completado não pode ser abandonado diretamente."
            )
        self.status = GameStatus(GameStatus.DROPPED)
        self.completed_date = None
        self._ensure_consistency()

    def reopen(self) -> None:
        """Reabre um jogo concluído para permitir novo progresso."""
        if self.status.value != GameStatus.COMPLETED:
            raise DomainException("Apenas jogos completados podem ser reabertos.")
        self.status = GameStatus(GameStatus.PLAYING)
        self.completed_date = None
        self._ensure_consistency()

    def rate(self, rating: Any) -> None:
        """Registra a avaliação pessoal do usuário."""
        self.user_rating = GameRating(rating)
        self._ensure_consistency()

    def _ensure_consistency(self) -> None:
        if self.status.value == GameStatus.WISHLIST:
            if self.progress.value != 0 or self.hours_played.value != 0:
                raise DomainException(
                    "Jogos em wishlist devem iniciar sem progresso e sem horas jogadas."
                )
        if self.status.value == GameStatus.COMPLETED:
            if self.progress.value != 100:
                raise DomainException(
                    "Jogos completados devem ter progresso igual a 100."
                )
            if self.completed_date is None:
                raise DomainException(
                    "Jogos completados devem possuir data de conclusão."
                )
            if self.user_rating.value is None:
                raise DomainException(
                    "Jogos completados devem possuir avaliação pessoal."
                )
        if (
            self.status.value != GameStatus.COMPLETED
            and self.completed_date is not None
        ):
            raise DomainException(
                "A data de conclusão só pode existir para jogos completados."
            )
