# Trabalho-DDD


# Documentação do Modelo de Domínio - Projeto Katalog

1. Descrição do Case

O **Katalog** é um sistema de gerenciamento de acervo pessoal para monitorar o consumo de mídias (filmes, jogos e livros). O objetivo central desta evolução é garantir que as regras de progresso e avaliação de mídias estejam protegidas dentro de um domínio isolado, livre de dependências técnicas.

2. Linguagem Ubíqua

| Termo | Significado no domínio |
| --- | --- |
| **Mídia** | Objeto principal do catálogo (filme, jogo ou livro).

 |
| **Progresso** | Medida de quanto da mídia já foi consumido (páginas, minutos ou %).

 |
| **Status** | Estado atual da mídia (Pendente, Em Andamento, Concluído).

 |
| **Invariante** | Regra de negócio que deve ser sempre verdadeira para manter a consistência.

 |

3. Módulos

Módulo: `Catalog`

* 
**Descrição**: Responsável pela gestão do acervo e das regras de evolução do consumo.


* **Classes incluídas**: `Midia`, `Progresso`, `Nota`, `StatusMidia`.
* 
**Justificativa**: Agrupa elementos que compartilham o mesmo significado de negócio: a organização e monitoramento de obras.



4. Entities

 Entity: `Midia`

* 
**Identidade**: Possui um `MidiaId` único e persistente.


* 
**Responsabilidades**: Controlar o ciclo de vida da obra no catálogo e validar mudanças de status.


* 
**Motivo para ser Entity**: Mesmo que o título ou o progresso mudem, a mídia continua sendo o mesmo objeto único no acervo do usuário.



5. Value Objects

Value Object: `Progresso`

* **Atributos**: `atual`, `total`.
* 
**Validações**: O valor atual não pode ser negativo nem superior ao total.


* 
**Motivo para ser Value Object**: É definido apenas por seus valores; dois progressos de "50/100" são idênticos em qualquer lugar.



### Value Object: `Nota`

* **Atributos**: `valor`.
* 
**Validações**: Deve estar entre 0 e 10.


* 
**Motivo para ser Value Object**: Representa apenas uma classificação qualitativa sem identidade própria.



 6. Aggregates

 Aggregate: `CatalogMidia`

* 
**Aggregate Root**: `Midia`.


* 
**Objetos internos**: `Progresso`, `Nota`, `StatusMidia`.


* **Invariantes protegidas**:
1. Uma mídia só pode ser "Concluída" se o progresso atingir 100%.


2. Não é permitido finalizar uma mídia sem atribuir uma nota.




* 
**Justificativa**: A `Midia` deve controlar o acesso ao `Progresso` para garantir que o status não fique inconsistente com os dados.



## 7. Factories

### Factory: `MidiaFactory`

* 
**Objeto criado**: `Midia` (Aggregate Root).


* 
**Motivo**: Garante que uma mídia sempre nasça com um estado inicial válido (Pendente e Progresso Zero).



8. Repositories

### Repository: `IMidiaRepository`

* 
**Aggregate persistido**: `Midia` (Root).


* 
**Motivo para existir**: Abstrair a persistência (Django ORM) da lógica de domínio.


* 
**Implementação**: A interface fica no `Domain` e a implementação concreta na `Infrastructure`.



 9. Regras de Negócio no Domínio

| Regra de negócio | Classe onde foi implementada |
| --- | --- |
| Progresso atual não pode exceder o total | <br>`Progresso` 

 |
| Nota deve ser entre 0 e 10 | <br>`Nota` 

 |
| Mídia concluída exige nota obrigatória | <br>`Midia` 

 |
| Bloqueio de finalização se progresso < 100% | <br>`Midia` 

 |

10. Decisões de Modelagem e Trade-offs

* **Decisão**: Isolamento total do Django. As classes de domínio são Python puro, sem herdar de `models.Model`, para garantir que o domínio não dependa de frameworks.


* 
**Trade-off**: Isso exige um mapeamento manual de dados entre o Domínio e a Infraestrutura (Mappers), aumentando a quantidade de código, mas garantindo a sustentabilidade exigida.
