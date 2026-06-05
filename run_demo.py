from katalog.domain.factories import MidiaFactory
from katalog.infrastructure.in_memory_repository import InMemoryMidiaRepository
from application.services import CatalogoApplicationService


def main():
    repo = InMemoryMidiaRepository()
    service = CatalogoApplicationService(repo)

    # adicionar mídia
    nova = service.adicionar_midia('Livro Demo', 100)
    print('Criada mídia:', nova.id, nova.titulo, nova.status)

    # atualizar consumo
    service.atualizar_consumo(str(nova.id), 25)
    midia = repo.buscar_por_id(str(nova.id))
    print('Progresso:', midia.progresso.atual, '/', midia.progresso.total, '-', midia.status)

    # tentar concluir antes do completo (deve falhar)
    try:
        service.concluir_obra(str(nova.id), 8)
    except Exception as e:
        print('Erro esperado ao concluir antes do completo:', e)

    # completar e concluir
    service.atualizar_consumo(str(nova.id), 100)
    service.concluir_obra(str(nova.id), 9)
    midia = repo.buscar_por_id(str(nova.id))
    print('Após conclusão:', midia.status, 'Nota:', midia.nota.valor)


if __name__ == '__main__':
    main()
