import uuid
from enum import Enum
from .value_objects import Progresso, Nota


class StatusMidia(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"


class Midia:
    """Entity e Aggregate Root: protege invariantes e expõe comportamentos."""
    def __init__(self, titulo: str, total_unidades: int, id=None):
        self.id = id or uuid.uuid4()
        self.titulo = titulo
        self.progresso = Progresso(0, total_unidades)
        self._status = StatusMidia.PENDENTE
        self.nota = None

    @property
    def status(self) -> StatusMidia:
        return self._status

    def registrar_progresso(self, novo_valor: int):
        """Atualiza progresso; protege transição de status."""
        self.progresso = Progresso(novo_valor, self.progresso.total)
        if self.progresso.atual > 0 and not self.progresso.is_completado():
            self._status = StatusMidia.EM_ANDAMENTO

    def percentual_consumido(self) -> float:
        """Consulta sem efeitos colaterais."""
        if self.progresso.total == 0:
            return 0.0
        return (self.progresso.atual / self.progresso.total) * 100

    def concluir(self, valor_nota: int):
        """Finaliza a mídia apenas se o progresso estiver completo."""
        if not self.progresso.is_completado():
            raise ValueError("Não é possível concluir uma mídia incompleta.")

        self.nota = Nota(valor_nota)
        self._status = StatusMidia.CONCLUIDO
