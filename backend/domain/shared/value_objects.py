from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .exceptions import DomainException


@dataclass(frozen=True)
class MediaTitle:
    value: str

    def __post_init__(self):
        normalized = (self.value or "").strip()
        if not normalized:
            raise DomainException("O título do jogo é obrigatório.")
        if len(normalized) > 200:
            raise DomainException("O título do jogo deve ter no máximo 200 caracteres.")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ReleaseYear:
    value: int

    def __post_init__(self):
        current_year = date.today().year
        if not isinstance(self.value, int):
            raise DomainException("O ano de lançamento deve ser numérico.")
        if self.value < 1950:
            raise DomainException("O ano de lançamento não pode ser anterior a 1950.")
        if self.value > current_year + 3:
            raise DomainException("O ano de lançamento não pode estar muito distante no futuro.")

    def __int__(self) -> int:
        return self.value
