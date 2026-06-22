```
Media Vault - Arquitetura do Projeto
═════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Browser)                         │
│                     React + Tailwind CSS                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                   API Gateway / Nginx Reversa                    │
│                    (Em produção com Docker)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
    ┌────────────────────────┼────────────────────────┐
    │                        │                        │
    ↓                        ↓                        ↓
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│  Django     │      │  PostgreSQL  │      │    Redis     │
│  Backend    │←────→│   Database   │      │    Cache/    │
│ REST API    │      │              │      │   Message    │
└─────────────┘      └──────────────┘      │    Broker    │
     ↑                                      │   (Celery)   │
     │                                      └──────────────┘
     │
  ┌──┴──────────────────────────────────────────┐
  │         Django Apps                          │
  ├──────────────────────────────────────────────┤
  │  📱 movies/        - Gerenciamento de filmes  │
  │  🎮 games/         - Gerenciamento de jogos   │
  │  👤 users/         - Perfil de usuários       │
  │  ⭐ ratings/       - Avaliações genéricas    │
  └──────────────────────────────────────────────┘

╔═════════════════════════════════════════════════════════════════╗
║           FLUXO DE DADOS - Exemplo: Cadastro de Filme          ║
╚═════════════════════════════════════════════════════════════════╝

1. Usuário no React Frontend
   └─> Preenche formulário de novo filme
       └─> Valida campos no cliente
           └─> Envia POST request /api/movies/

2. API Django Recebe
   └─> Autenticação JWT (verifica token)
       └─> Validação de dados (Serializer)
           └─> Salva no banco de dados
               └─> Retorna 201 Created

3. Banco de Dados (PostgreSQL)
   └─> Armazena: title, genres, year, rating, etc
       └─> Associa ao usuário (Foreign Key)
           └─> Cria timestamp de criação

4. Frontend Atualiza
   └─> Recebe resposta com ID do novo filme
       └─> Atualiza lista de filmes
           └─> Mostra confirmação ao usuário

╔═════════════════════════════════════════════════════════════════╗
║                 SEGURANÇA & AUTENTICAÇÃO                        ║
╚═════════════════════════════════════════════════════════════════╝

1. Registro/Login
   └─> POST /api/auth/register/
       └─> Hash da senha com bcrypt
           └─> Retorna token JWT

2. Requisições Autenticadas
   └─> Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
       └─> Django verifica token
           └─> Identifica usuário
               └─> Filtra dados apenas do usuário

3. Isolamento de Dados
   └─> Cada usuário vê apenas seus filmes
       └─> Não pode deletar/editar de outros
           └─> ViewSets filtram por user=request.user

╔═════════════════════════════════════════════════════════════════╗
║              DEPLOYMENT COM DOCKER COMPOSE                      ║
╚═════════════════════════════════════════════════════════════════╝

Serviços:
  ┌──────────────┐
  │  db          │  PostgreSQL 15 Alpine
  └──────┬───────┘
         │
  ┌──────┴───────┐
  │  redis       │  Redis 7 Alpine
  └──────┬───────┘
         │
  ┌──────┴───────────────────┐
  │  backend                 │  Django + Gunicorn + Python 3.11
  └──────┬─────────────────────┘
         │
  ┌──────┴────────────────────┐
  │  frontend                 │  React + Node 18 Alpine
  └───────────────────────────┘

Volumes:
  - postgres_data: Persistência do banco de dados
  - backend/: Live reload durante desenvolvimento
  - frontend/: Live reload durante desenvolvimento

Redes:
  - media_vault_network: Comunicação interna entre containers

╔═════════════════════════════════════════════════════════════════╗
║            CI/CD PIPELINE (GitHub Actions)                      ║
╚═════════════════════════════════════════════════════════════════╝

Ao fazer push/PR:
  1. Testes Backend
     └─> pytest com cobertura
         └─> PostgreSQL de teste

  2. Testes Frontend
     └─> npm test
         └─> ESLint

  3. Build Frontend
     └─> npm run build
         └─> Validação

╔═════════════════════════════════════════════════════════════════╗
║                    ESTRUTURA DE DADOS                           ║
╚═════════════════════════════════════════════════════════════════╝

Movie
├── id
├── title
├── genres
├── release_year
├── director
├── rating (IMDB/TMDB)
├── user_rating (avaliação pessoal)
├── status (watched, watching, wishlist)
├── watched_date
├── user (FK → User)
└── timestamps (created_at, updated_at)

Game
├── id
├── title
├── genres
├── platform (PC, PS5, Xbox, Switch)
├── developer
├── publisher
├── rating (IGDB)
├── user_rating
├── status (completed, playing, wishlist)
├── progress (0-100%)
├── hours_played
├── completed_date
├── user (FK → User)
└── timestamps

UserProfile
├── id
├── user (OneToOne → User)
├── bio
├── avatar
├── favorite_genre_movies
├── favorite_genre_games
├── favorite_platform
└── timestamps

Rating
├── id
├── user (FK → User)
├── content_type (Movie/Game)
├── object_id
├── rating (1-5 stars)
├── comment
└── timestamps
```

## 🚀 Próximos Passos para Iniciar

```bash
# 1. Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# 2. Frontend (novo terminal)
cd frontend
npm install
npm start

# 3. Ou tudo com Docker
docker-compose -f docker/docker-compose.yml up
```

## 📖 Documentação Auxiliar

- [README.md](../README.md) - Overview do projeto
- [docs/SETUP.md](../docs/SETUP.md) - Instruções de configuração
- [docs/API.md](../docs/API.md) - Documentação da API
- [STRUCTURE.md](../STRUCTURE.md) - Estrutura detalhada de pastas
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Guia de contribuição
```
