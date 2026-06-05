from .entities import Midia

class CatalogService:
    """Domain Service: lógica que não pertence a uma única entidade."""
    def duplicar_item_para_outro_usuario(self, midia_original: Midia):
        # cria nova mídia baseada em outra, mas reseta o progresso
        return Midia(titulo=f"Cópia de {midia_original.titulo}", 
                     total_unidades=midia_original.progresso.total)
