# Contribuindo para Media Vault

Obrigado por se interessar em contribuir para o Media Vault!

## Processo de Contribuição

1. Faça um Fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Padrões de Código

### Python/Django

- Utilize PEP 8
- Adicione type hints quando possível
- Escreva docstrings para funções e classes
- Mantenha linhas com no máximo 88 caracteres

### JavaScript/React

- Utilize ESLint
- Escreva componentes funcionais
- Use hooks ao invés de class components
- Mantenha componentes menores e reutilizáveis

## Testes

Antes de enviar um PR, certifique-se de:

1. Executar testes localmente
2. Manter cobertura de testes >= 80%
3. Verificar que testes passam na CI/CD

```bash
# Backend
pytest --cov=apps

# Frontend
npm test
```

## Issues e Bugs

Ao reportar bugs, inclua:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs observado
- Screenshots/logs se aplicável
- Sistema operacional e versão
- Navegador (se frontend) e versão

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a MIT License.
