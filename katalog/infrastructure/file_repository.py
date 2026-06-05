import pickle
from pathlib import Path
from typing import Optional
from katalog.domain.repositories import IMidiaRepository
from katalog.domain.entities import Midia


class FileBasedMidiaRepository(IMidiaRepository):
    def __init__(self, folder: str = '.data'):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

    def _path(self, midia_id: str) -> Path:
        return self.folder / f"{midia_id}.pkl"

    def salvar(self, midia: Midia):
        p = self._path(str(midia.id))
        with p.open('wb') as f:
            pickle.dump(midia, f)

    def buscar_por_id(self, midia_id: str) -> Midia:
        p = self._path(str(midia_id))
        if not p.exists():
            raise KeyError(f"Mídia {midia_id} não encontrada")
        with p.open('rb') as f:
            return pickle.load(f)
