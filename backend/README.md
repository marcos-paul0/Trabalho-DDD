# Backend - Django API para Media Vault

API REST para gerenciar filmes e jogos pessoais.

## Estrutura

```
backend/
├── media_vault/          # Configurações principais
├── apps/
│   ├── movies/          # App de filmes
│   ├── games/           # App de jogos
│   ├── users/           # App de usuários
│   └── ratings/         # App de avaliações
├── tests/               # Testes
├── manage.py
└── requirements.txt
```

## Instalação

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuração

```bash
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
```

## Executar

```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`

## Admin

Acesse o painel admin em `http://localhost:8000/admin`

## Testes

```bash
pytest
pytest --cov=apps
```

## Documentação

Veja [API.md](../docs/API.md) para documentação completa da API.
