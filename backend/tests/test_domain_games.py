from datetime import date

import pytest

from domain.catalog.games.factories import GameCatalogItemFactory
from domain.catalog.games.services import GameProgressService
from domain.shared.exceptions import DomainException


def test_game_wishlist_deve_iniciar_sem_progresso_e_horas():
    with pytest.raises(DomainException):
        GameCatalogItemFactory.create(
            user_id=1,
            title="Hollow Knight",
            platform="pc",
            release_year=2017,
            genres="indie",
            status="wishlist",
            progress=10,
            hours_played=1,
        )


def test_game_completado_deve_ter_progresso_100_data_e_avaliacao():
    game = GameCatalogItemFactory.create(
        user_id=1,
        title="Celeste",
        platform="switch",
        release_year=2018,
        genres="indie",
        status="completed",
        user_rating=5,
    )

    assert game.progress.value == 100
    assert game.completed_date is not None
    assert game.user_rating.value == 5
    assert game.status.value == "completed"


def test_nao_pode_concluir_sem_avaliacao_pessoal():
    game = GameCatalogItemFactory.create(
        user_id=1,
        title="Elden Ring",
        platform="ps5",
        release_year=2022,
        genres="rpg",
        status="playing",
    )

    with pytest.raises(DomainException):
        game.update_progress(100)


def test_update_progress_para_100_completa_jogo_ja_avaliado():
    game = GameCatalogItemFactory.create(
        user_id=1,
        title="Elden Ring",
        platform="ps5",
        release_year=2022,
        genres="rpg",
        status="playing",
        user_rating=5,
    )

    game.update_progress(100)

    assert game.status.value == "completed"
    assert game.progress.value == 100
    assert game.completed_date == date.today()


def test_rating_deve_ficar_entre_0_e_5():
    game = GameCatalogItemFactory.create(
        user_id=1,
        title="Forza Horizon",
        platform="xbox-series",
        release_year=2021,
        genres="racing",
    )

    with pytest.raises(DomainException):
        game.rate(7)


def test_register_play_session_soma_horas_e_inicia_jogo():
    game = GameCatalogItemFactory.create(
        user_id=1,
        title="Hades",
        platform="pc",
        release_year=2020,
        genres="indie",
        status="wishlist",
    )

    GameProgressService().register_play_session(game, hours=2, progress=15)

    assert game.hours_played.value == 2
    assert game.progress.value == 15
    assert game.status.value == "playing"


def test_jogo_abandonado_precisa_ser_retomado_antes_de_sessao():
    game = GameCatalogItemFactory.create(
        user_id=1,
        title="Darkest Dungeon",
        platform="pc",
        release_year=2016,
        genres="rpg",
        status="playing",
    )
    game.drop()

    with pytest.raises(DomainException):
        GameProgressService().register_play_session(game, hours=1, progress=20)
