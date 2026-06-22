# Documentação da API - Media Vault

## Autenticação

Todos os endpoints (exceto registro e login) requerem autenticação via JWT.

### Registrar novo usuário

```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "seu_usuario",
  "email": "seu@email.com",
  "password": "sua_senha",
  "password_confirm": "sua_senha"
}
```

### Fazer Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}

Response:
{
  "access": "seu_token_jwt",
  "refresh": "seu_token_refresh"
}
```

## Filmes

### Listar todos os filmes

```http
GET /api/movies/
Authorization: Bearer {token}
```

### Criar novo filme

```http
POST /api/movies/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Inception",
  "description": "Um ladrão que rouba segredos corporativos...",
  "genres": "Sci-Fi, Action",
  "release_year": 2010,
  "director": "Christopher Nolan",
  "status": "watched",
  "user_rating": 4.5,
  "poster_url": "https://..."
}
```

### Buscar filme por ID

```http
GET /api/movies/{id}/
Authorization: Bearer {token}
```

### Atualizar filme

```http
PUT /api/movies/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Inception",
  "user_rating": 5.0,
  "status": "watched"
}
```

### Deletar filme

```http
DELETE /api/movies/{id}/
Authorization: Bearer {token}
```

### Buscar filmes

```http
GET /api/movies/search/?q=inception
Authorization: Bearer {token}
```

### Listar por status

```http
GET /api/movies/by_status/?status=watched
Authorization: Bearer {token}
```

### Estatísticas de filmes

```http
GET /api/movies/statistics/
Authorization: Bearer {token}
```

## Jogos

Mesma estrutura que filmes, mas com endpoints em `/api/games/`

Campos adicionais para jogos:
- `platform`: PC, PS4, PS5, Xbox One, Xbox Series, Switch, Mobile
- `developer`: Nome da desenvolvedora
- `publisher`: Nome da publicadora
- `progress`: Porcentagem de conclusão (0-100)
- `hours_played`: Horas jogadas
- `completed_date`: Data de conclusão

### Listar por plataforma

```http
GET /api/games/by_platform/?platform=ps5
Authorization: Bearer {token}
```

### Estatísticas de jogos

```http
GET /api/games/statistics/
Authorization: Bearer {token}
```

## Perfil do Usuário

### Obter perfil

```http
GET /api/users/profile/
Authorization: Bearer {token}
```

### Atualizar perfil

```http
PUT /api/users/profile/
Authorization: Bearer {token}
Content-Type: application/json

{
  "first_name": "Seu Nome",
  "email": "novo@email.com"
}
```

### Estatísticas gerais

```http
GET /api/users/statistics/
Authorization: Bearer {token}
```

## Avaliações

### Criar/Atualizar avaliação

```http
POST /api/ratings/
Authorization: Bearer {token}
Content-Type: application/json

{
  "content_type": 5,  # ID do ContentType (films=5, games=6)
  "object_id": 1,     # ID do filme ou jogo
  "rating": 5,        # Rating de 1 a 5
  "comment": "Filme incrível!"
}
```

### Listar minhas avaliações

```http
GET /api/ratings/
Authorization: Bearer {token}
```

## Códigos de Resposta

- `200 OK` - Sucesso
- `201 Created` - Recurso criado com sucesso
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Não autenticado
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Recurso não encontrado
- `500 Internal Server Error` - Erro no servidor
