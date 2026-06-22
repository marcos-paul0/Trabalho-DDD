# Frontend - React para Media Vault

Interface web para gerenciar sua biblioteca de filmes e jogos.

## Estrutura

```
frontend/
├── public/
│   └── index.html       # HTML base
├── src/
│   ├── components/      # Componentes React
│   ├── pages/           # Páginas
│   ├── services/        # Serviços API
│   ├── App.js
│   └── index.js
├── package.json
└── Dockerfile.dev
```

## Instalação

```bash
cd frontend
npm install
```

## Development

```bash
npm start
```

A aplicação estará disponível em `http://localhost:3000`

## Build

```bash
npm run build
```

Gera a versão otimizada em `build/`

## Variáveis de Ambiente

Crie um arquivo `.env`:

```
REACT_APP_API_URL=http://localhost:8000/api
```

## Docker

```bash
docker build -f Dockerfile.dev -t media-vault-frontend .
docker run -p 3000:3000 media-vault-frontend
```
