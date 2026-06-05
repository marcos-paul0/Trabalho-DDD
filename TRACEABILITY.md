# Tabela de Rastreabilidade - Regras de Negócio -> Código / Testes

Regra de negócio | Classe / Método | Teste existente | Observações
---|---|---|---
Mídia incompleta não pode ser concluída | `Midia.concluir()` ([katalog/domain/entities.py](katalog/domain/entities.py#L1)) | `tests/test_domain.py::DomainTests::test_concluir_somente_completo` | Implementada e testada
Progresso deve estar no intervalo válido | `Progresso` ([katalog/domain/value_objects.py](katalog/domain/value_objects.py#L1)) | `tests/test_domain.py::DomainTests::test_progresso_invalido` | Implementada e testada
Nota entre 0 e 10 | `Nota` ([katalog/domain/value_objects.py](katalog/domain/value_objects.py#L1)) | `tests/test_domain.py::DomainTests::test_nota_invalida` | Implementada e testada
Status do agregado deve ser controlado | `Midia.status` (`StatusMidia` enum) | `tests/test_domain.py::DomainTests::test_midia_registra_progresso_e_percentual` | Implementada e testada
Persistência em memória para desenvolvimento/testes | `InMemoryMidiaRepository` ([katalog/infrastructure/in_memory_repository.py](katalog/infrastructure/in_memory_repository.py)) | `tests/test_repository.py` (novo) | Implementada
Persistência em arquivo para demo | `FileBasedMidiaRepository` ([katalog/infrastructure/file_repository.py](katalog/infrastructure/file_repository.py)) | `tests/test_repository.py` (novo) | Implementada
