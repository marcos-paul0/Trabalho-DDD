from .entities import Midia

class MidiaFactory:
    """Factory: garante a criação correta de uma nova mídia."""
    @staticmethod
    def criar_item(titulo: str, total: int) -> Midia:
        if not titulo:
            raise ValueError("A mídia precisa de um título.")
        return Midia(titulo=titulo, total_unidades=total)
