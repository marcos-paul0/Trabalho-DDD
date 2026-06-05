from abc import ABC, abstractmethod
from katalog.domain.entities import Midia

class IMidiaRepository(ABC):
    """Classe 5: Interface do Repositório (Port)."""
    @abstractmethod
    def salvar(self, midia: Midia):
        pass

    @abstractmethod
    def buscar_por_id(self, midia_id: str) -> Midia:
        pass
