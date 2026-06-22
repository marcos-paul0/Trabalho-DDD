# Roteiro de Apresentação - Evolução DDD

Tempo sugerido: até 10 minutos.

## 1. Abertura - problema do case

O sistema Media Vault/Katalog é um catálogo pessoal de mídias. Ele permite que usuários cadastrem filmes e jogos, acompanhem status, progresso e avaliações pessoais.

Para a atividade de Domain-Driven Design, escolhemos como funcionalidade principal o **gerenciamento do ciclo de vida de jogos no catálogo pessoal do usuário**.

Esse recorte foi escolhido porque possui regras de domínio claras, como status do jogo, progresso, horas jogadas, avaliação e conclusão.

## 2. Situação anterior

Antes da evolução, a estrutura seguia o padrão tradicional do Django:

```text
Model → Serializer → ViewSet → Banco
```

O problema é que isso deixava o domínio muito acoplado ao Django ORM e à API. O model `Game` funcionava como modelo de persistência e também como representação do negócio.

Com a evolução, separamos o domínio das preocupações técnicas.

## 3. Nova estrutura em camadas

A estrutura criada foi:

```text
backend/
 ├── domain/
 ├── application/
 ├── infrastructure/
 └── apps/
```

- `domain`: contém regras e conceitos do negócio.
- `application`: coordena os casos de uso.
- `infrastructure`: implementa detalhes técnicos, como persistência com Django ORM.
- `apps/games`: continua responsável pela API com Django REST Framework.

## 4. Linguagem ubíqua

Os principais termos do domínio são:

- Jogo
- Catálogo
- Plataforma
- Progresso
- Horas jogadas
- Wishlist
- Jogando
- Completado
- Abandonado
- Avaliação pessoal
- Data de conclusão

Esses termos aparecem no código e na documentação para manter alinhamento entre negócio e implementação.

## 5. Entity principal

A principal Entity criada foi `GameCatalogItem`.

Ela representa um jogo dentro do catálogo pessoal de um usuário.

Ela foi modelada como Entity porque possui:

- identidade própria;
- ciclo de vida;
- mudança de estado;
- comportamentos;
- regras de negócio.

Exemplos de comportamentos:

- `start_playing()`
- `update_progress()`
- `add_played_hours()`
- `complete()`
- `drop()`
- `reopen()`
- `rate()`

## 6. Value Objects

Foram criados Value Objects para proteger conceitos do domínio:

- `MediaTitle`: valida título obrigatório e tamanho máximo.
- `ReleaseYear`: valida ano de lançamento.
- `Platform`: valida plataformas permitidas.
- `GameStatus`: valida status permitidos.
- `ProgressPercentage`: valida progresso entre 0 e 100.
- `HoursPlayed`: impede horas negativas.
- `GameRating`: valida avaliação entre 0 e 5.

Esses objetos não possuem identidade própria. Eles são definidos pelos seus valores.

## 7. Aggregate e Aggregate Root

O Aggregate escolhido foi `GameCatalogItem`.

A Aggregate Root também é `GameCatalogItem`, porque ela controla as alterações de status, progresso, horas jogadas, avaliação e data de conclusão.

As principais invariantes protegidas são:

- jogo completado deve ter progresso 100;
- jogo completado deve possuir data de conclusão;
- jogo em wishlist não pode ter progresso nem horas jogadas;
- progresso sempre deve estar entre 0 e 100;
- avaliação deve estar entre 0 e 5;
- data de conclusão só pode existir em jogo completado.

## 8. Factory

A Factory criada foi `GameCatalogItemFactory`.

Ela existe porque criar um jogo envolve regras iniciais. Por exemplo:

- se o status inicial for `completed`, o progresso deve ser 100;
- se o status for `completed` e não houver data, a data atual é preenchida;
- se o status for `wishlist`, o jogo precisa começar sem progresso e sem horas jogadas.

Assim, o objeto não nasce em estado inválido.

## 9. Domain Service

O Domain Service criado foi `GameProgressService`.

Ele representa a política de atualização de progresso e horas jogadas.

Ele foi separado porque essa regra pode envolver transição de status. Por exemplo, quando o progresso chega a 100, o jogo é marcado como completado.

Esse serviço não acessa banco de dados, não usa Django e não depende de infraestrutura.

## 10. Repository

Foi criada a interface `GameCatalogRepository` dentro do domínio.

A implementação concreta é `DjangoGameCatalogRepository`, localizada em infraestrutura.

Esse repositório converte:

```text
Django Model ↔ Domain Entity
```

Assim, o domínio não conhece o Django ORM.

## 11. Casos de uso

Na camada de aplicação foram criados:

- `CreateGameUseCase`
- `UpdateGameUseCase`
- `UpdateGameProgressUseCase`
- `RateGameUseCase`

Eles coordenam o fluxo, mas não concentram regra de negócio central. A regra fica no domínio.

## 12. Exemplo de regra demonstrável

Se o usuário tentar informar progresso `150`, o domínio rejeita porque `ProgressPercentage` exige valor entre 0 e 100.

Se o usuário tentar informar avaliação `8`, o domínio rejeita porque `GameRating` permite apenas valores entre 0 e 5.

Se um jogo estiver como `wishlist`, ele não pode nascer com horas jogadas ou progresso maior que zero.

## 13. Decisões importantes

A principal decisão foi não reescrever o sistema inteiro. Mantivemos Django e DRF funcionando, mas movemos o conhecimento principal do negócio para uma camada de domínio isolada.

Outra decisão foi focar em jogos, pois esse recorte possui mais regras de ciclo de vida do que filmes.

## 14. Trade-offs

O projeto ainda mantém models Django para persistência. Isso é intencional: eles não representam mais o domínio puro, mas sim o mecanismo de armazenamento.

A evolução foi incremental para manter o sistema funcional e evitar uma refatoração grande demais para o escopo da atividade.

## 15. Fechamento

Com essa evolução, o projeto deixa de ser apenas um CRUD de jogos e passa a expressar regras de negócio em um modelo de domínio mais claro, testável e sustentável.
