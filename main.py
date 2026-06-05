from katalog.domain.factories import MidiaFactory
from katalog.domain.services import CatalogService

def exemplo_simples():
    # Demonstração mínima de criação de mídia via factory
    m = MidiaFactory.criar_item('Exemplo Main', 10)
    print('Mídia criada:', m.id, m.titulo)

if __name__ == '__main__':
    exemplo_simples()