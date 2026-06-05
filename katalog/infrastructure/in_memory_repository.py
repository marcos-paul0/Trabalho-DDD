from typing import Dict
from katalog.domain.repositories import IMidiaRepository
from katalog.domain.entities import Midia


class InMemoryMidiaRepository(IMidiaRepository):
    def __init__(self):
        self._store: Dict[str, Midia] = {}

    def salvar(self, midia: Midia):
        # usa string do uuid como chave
        self._store[str(midia.id)] = midia

    def buscar_por_id(self, midia_id: str) -> Midia:
        item = self._store.get(str(midia_id))
        if item is None:
            raise KeyError(f"Mídia {midia_id} não encontrada")
        return item
