from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from domain.shared.exceptions import DomainException


@dataclass(frozen=True)
class Platform:
    value: str

    ALLOWED = {
        "pc",
        "ps4",
        "ps5",
        "xbox-one",
        "xbox-series",
        "switch",
        "mobile",
    }

    def __post_init__(self):
        normalized = (self.value or "").strip().lower()
        if normalized not in self.ALLOWED:
            raise DomainException("A plataforma informada não pertence ao catálogo permitido.")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class GameStatus:
    value: str

    WISHLIST = "wishlist"
    PLAYING = "playing"
    COMPLETED = "completed"
    DROPPED = "dropped"
    ALLOWED = {WISHLIST, PLAYING, COMPLETED, DROPPED}

    def __post_init__(self):
        normalized = (self.value or "").strip().lower()
        if normalized not in self.ALLOWED:
            raise DomainException("O status do jogo é inválido.")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ProgressPercentage:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise DomainException("O progresso deve ser um número inteiro.")
        if self.value < 0 or self.value > 100:
            raise DomainException("O progresso deve estar entre 0 e 100.")

    def __int__(self) -> int:
        return self.value


@dataclass(frozen=True)
class HoursPlayed:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise DomainException("As horas jogadas devem ser um número inteiro.")
        if self.value < 0:
            raise DomainException("As horas jogadas não podem ser negativas.")

    def add(self, other: "HoursPlayed") -> "HoursPlayed":
        return HoursPlayed(self.value + other.value)

    def __int__(self) -> int:
        return self.value


@dataclass(frozen=True)
class GameRating:
    value: Decimal | None

    def __post_init__(self):
        if self.value is None or self.value == "":
            object.__setattr__(self, "value", None)
            return
        try:
            decimal_value = Decimal(str(self.value))
        except (InvalidOperation, ValueError):
            raise DomainException("A avaliação deve ser numérica.")
        if decimal_value < Decimal("0") or decimal_value > Decimal("5"):
            raise DomainException("A avaliação do usuário deve estar entre 0 e 5.")
        object.__setattr__(self, "value", decimal_value)

    def as_decimal(self) -> Decimal | None:
        return self.value
