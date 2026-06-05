# Design Decisions — Katalog

Este documento registra principais decisões, alternativas consideradas e justificativas.

1. `StatusMidia` como `Enum` (decisão)
- Por que: evita strings soltas, melhora expressividade e previne erros.
- Alternativas: Value Object com validação; preferido Enum pela simplicidade.

2. Manter `MidiaFactory` (decisão)
- Por que: atualmente criação é simples, mas a Factory oferece ponto central para regras futuras (ex.: criação com relacionamentos ou valores padrão). A Factory foi mantida e documentada.
- Alternativas: remover e usar o construtor diretamente.

3. Repositórios
- Implementado `InMemoryMidiaRepository` para testes e `FileBasedMidiaRepository` para persistência simples sem infra adicional.
- Futuro: adicionar adaptadores para bancos relacionais ou NoSQL se necessário.

4. Testes
- Foram adicionados testes unitários usando `unittest` para evitar dependência de ferramentas externas.

5. Packaging e entrypoint
- `main.py` foi simplificado para evitar manipulação manual de `sys.path`. Recomendado criar `pyproject.toml` e empacotar adequadamente.

6. Trade-offs não resolvidos
- Reorganizar a estrutura em pastas por subdomínio (ex.: `catalog/` com domínio, aplicação, infra) não foi realizado para evitar mudanças de escopo; porém, é recomendado para projetos maiores.

Documentação complementar e diagramas foram adicionados ao repositório.
