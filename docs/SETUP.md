# Guia de Configuração - Media Vault

## Requisitos do Sistema

- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- Node.js 16+ (para o frontend)

## Instalação Local

### 1. Backend Django

```bash
# Navegue até a pasta do backend
cd backend

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

### 2. Frontend React

```bash
cd frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm start
```

## Usando Docker

```bash
docker-compose -f docker/docker-compose.yml up -d
```

Acesse:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Admin Django: http://localhost:8000/admin
