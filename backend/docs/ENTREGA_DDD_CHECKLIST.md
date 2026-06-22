# Checklist da Entrega Final DDD

Este checklist organiza os pontos conferidos para a versão final do projeto Katalog/Media Vault na Entrega 3.

## 1. Escopo escolhido

- [x] Funcionalidade principal escolhida: **gerenciamento do ciclo de vida de jogos no catálogo pessoal do usuário**.
- [x] O recorte evita refatorar o sistema inteiro e concentra a entrega em uma parte do domínio com regras reais.
- [x] A escolha está documentada em `backend/docs/DOMAIN_MODEL_DDD.md`.
- [x] A entrega final está documentada em `ENTREGA_FINAL.md`.

## 2. Domínio isolado

- [x] Camada de domínio criada em `backend/domain`.
- [x] Domínio não importa Django, DRF, ORM, serializers, views ou banco de dados.
- [x] Exceções de domínio centralizadas em `domain/shared/exceptions.py`.
- [x] Regras principais estão em Entities, Value Objects e Domain Service.
- [x] A persistência concreta está fora do domínio.

## 3. Camadas

```text
backend/
 ├── domain/
 │   ├── shared/
 │   └── catalog/games/
 ├── application/
 │   └── catalog/games/
 ├── infrastructure/
 │   └── persistence/
 └── apps/
     └── games/
```

- [x] `domain`: regras e modelo de negócio.
- [x] `application`: casos de uso e DTOs.
- [x] `infrastructure`: repositório concreto com Django ORM.
- [x] `apps/games`: API Django/DRF chamando casos de uso.

## 4. Entity

- [x] `GameCatalogItem` criado como Entity e Aggregate Root.
- [x] Possui identidade (`id`).
- [x] Possui ciclo de vida.
- [x] Possui comportamentos, não apenas atributos.
- [x] Controla mudanças de estado como iniciar, concluir, abandonar, reabrir e avaliar.

## 5. Value Objects

- [x] `MediaTitle`
- [x] `ReleaseYear`
- [x] `Platform`
- [x] `GameStatus`
- [x] `ProgressPercentage`
- [x] `HoursPlayed`
- [x] `GameRating`

Todos possuem validações próprias e são modelados por valor, não por identidade.

## 6. Aggregate e Aggregate Root

- [x] Aggregate definido: `GameCatalogItem`.
- [x] Aggregate Root: `GameCatalogItem`.
- [x] Objetos internos protegidos por Value Objects.
- [x] Alterações relevantes passam por métodos da Aggregate Root ou pelo Domain Service.
- [x] Invariantes documentadas em `DOMAIN_MODEL_DDD.md` e `ENTREGA_FINAL.md`.

## 7. Factory

- [x] `GameCatalogItemFactory` criada.
- [x] Cria jogos em estado inicial válido.
- [x] Centraliza regras de criação relacionadas a status, progresso, avaliação e data de conclusão.

## 8. Domain Service

- [x] `GameProgressService` criado.
- [x] Operação principal ajustada para `register_play_session`.
- [x] Representa uma sessão real de jogo, combinando horas jogadas e progresso opcional.
- [x] Não depende de infraestrutura.
- [x] Não substitui a Entity, apenas coordena uma operação específica de domínio.

## 9. Repositories

- [x] Interface `GameCatalogRepository` criada no domínio.
- [x] Implementação concreta `DjangoGameCatalogRepository` criada em infraestrutura.
- [x] Repository trabalha com a Aggregate Root `GameCatalogItem`.
- [x] Conversão entre Django Model e Domain Entity fica fora do domínio.

## 10. Application Use Cases

- [x] `CreateGameUseCase`
- [x] `UpdateGameUseCase`
- [x] `UpdateGameProgressUseCase`
- [x] `RegisterPlaySessionUseCase`
- [x] `RateGameUseCase`

Os casos de uso coordenam o fluxo, buscam/salvam pelo Repository e delegam regras ao domínio.

## 11. API atualizada

- [x] `POST /api/games/` passa pelo domínio.
- [x] `PUT /api/games/{id}/` passa pelo domínio.
- [x] `PATCH /api/games/{id}/` passa pelo domínio.
- [x] `PATCH /api/games/{id}/update_progress/` passa pelo domínio.
- [x] `PATCH /api/games/{id}/register_session/` passa pelo domínio.
- [x] `PATCH /api/games/{id}/rate/` passa pelo domínio.

## 12. Regras de negócio rastreáveis

| Regra | Implementação |
|---|---|
| Título obrigatório | `MediaTitle` |
| Ano de lançamento válido | `ReleaseYear` |
| Plataforma permitida | `Platform` |
| Status permitido | `GameStatus` |
| Progresso entre 0 e 100 | `ProgressPercentage` |
| Horas não negativas | `HoursPlayed` |
| Avaliação entre 0 e 5 | `GameRating` |
| Jogo completado com progresso 100 | `GameCatalogItem` |
| Jogo completado com data de conclusão | `GameCatalogItem` |
| Jogo completado com avaliação pessoal | `GameCatalogItem` |
| Wishlist sem progresso/horas | `GameCatalogItem` |
| Sessão de jogo respeitando status | `GameProgressService` |
| Persistência da Aggregate Root | `GameCatalogRepository` |

## 13. Testes

- [x] Testes de domínio criados em `backend/tests/test_domain_games.py`.
- [x] Testes de API de jogos criados em `backend/tests/test_api_games.py`.
- [x] Teste para impedir conclusão sem avaliação pessoal.
- [x] Teste para registrar sessão de jogo.
- [x] Teste para bloquear sessão em jogo abandonado.
- [x] `pytest` executado com sucesso.
- [x] `python manage.py check` executado com sucesso.

Comandos executados:

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest -q
python manage.py check
```

Resultado:

```text
27 passed
System check identified no issues (0 silenced).
```

## 14. Documentos da entrega

- [x] Código-fonte atualizado.
- [x] `ENTREGA_FINAL.md`.
- [x] `backend/docs/DOMAIN_MODEL_DDD.md`.
- [x] `backend/docs/ENTREGA_DDD_CHECKLIST.md`.
- [x] Diagrama Mermaid incluído na documentação.
- [x] Lista de regras de negócio incluída na documentação.
- [x] Instruções de execução incluídas na documentação.

## 15. Pontos pendentes para submissão no repositório final

- [ ] Preencher nomes dos integrantes em `ENTREGA_FINAL.md`.
- [ ] Preencher o link final do repositório em `ENTREGA_FINAL.md`.
- [ ] Fazer commits separados no GitHub com mensagens claras.
- [ ] Conferir o funcionamento no ambiente local do grupo.
