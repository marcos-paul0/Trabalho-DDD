from __future__ import annotations

from domain.shared.exceptions import DomainException

from .entities import GameCatalogItem
from .value_objects import GameStatus


class GameProgressService:
    """Serviço de domínio para registrar sessões de jogo.

    A operação de sessão combina horas jogadas, progresso opcional e política de
    retomada. Ela representa um conceito do domínio que não é apenas trocar um
    campo isolado da Entity.
    """

    def update_progress(self, game: GameCatalogItem, progress: int) -> None:
        """Atualiza somente o progresso mantendo a política central na Aggregate Root."""
        game.update_progress(progress)

    def register_play_session(
        self, game: GameCatalogItem, hours: int, progress: int | None = None
    ) -> None:
        """Registra uma sessão de jogo com horas e, opcionalmente, novo progresso."""
        if game.status.value == GameStatus.DROPPED:
            raise DomainException(
                "Não é possível registrar sessão em jogo abandonado sem retomá-lo."
            )
        game.add_played_hours(hours)
        if progress is not None:
            game.update_progress(progress)

    def add_hours_and_update_progress(
        self, game: GameCatalogItem, hours: int, progress: int | None = None
    ) -> None:
        """Compatibilidade com a refatoração anterior."""
        self.register_play_session(game, hours, progress)
