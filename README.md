# MyPace Backend API

API REST para gerenciamento de corridas do aplicativo MyPace, desenvolvida com Django REST Framework e PostgreSQL.

## 🚀 Stack Tecnológica

- **Python 3.12+**
- **Django 6.0** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** (Neon) - Banco de dados
- **drf-spectacular** - Documentação Swagger/OpenAPI
- **Gunicorn** - Servidor WSGI para produção
- **WhiteNoise** - Servir arquivos estáticos
- **UV** - Gerenciador de pacotes e ambientes

## 📋 Pré-requisitos

- Python 3.12 ou superior
- UV instalado ([https://docs.astral.sh/uv/](https://docs.astral.sh/uv/))
- Conta no Neon DB ([https://neon.tech](https://neon.tech))

## 🛠️ Setup Local

### 1. Clone o repositório

```bash
git clone https://github.com/carlosxfelipe/mypace-backend.git
cd mypace-backend
```

### 2. Instale as dependências

```bash
uv sync
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-secret-key-aqui
DEBUG=True
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

Para gerar uma `SECRET_KEY` segura:

```bash
uv run python - << 'EOF'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
EOF
```

### 4. Execute as migrações

```bash
uv run python manage.py migrate
```

### 5. Crie um superusuário

```bash
uv run python manage.py createsuperuser
```

### 6. Inicie o servidor de desenvolvimento

```bash
uv run python manage.py runserver
```

A API estará disponível em:

- **API:** http://localhost:8000/api/
- **Documentação:** http://localhost:8000/api/docs/
- **Admin:** http://localhost:8000/admin/

## 📡 Endpoints da API

### Autenticação (Públicos)

| Método | Endpoint              | Descrição              |
| ------ | --------------------- | ---------------------- |
| POST   | `/api/auth/register/` | Registrar novo usuário |
| POST   | `/api/auth/login/`    | Login (obter token)    |

### Conta (Requer Autenticação)

| Método | Endpoint                     | Descrição     |
| ------ | ---------------------------- | ------------- |
| PUT    | `/api/auth/change-password/` | Mudar senha   |
| DELETE | `/api/auth/delete-account/`  | Deletar conta |

### Corridas (Requer Autenticação)

| Método | Endpoint           | Descrição                 |
| ------ | ------------------ | ------------------------- |
| GET    | `/api/runs/`       | Listar corridas           |
| POST   | `/api/runs/`       | Criar corrida             |
| GET    | `/api/runs/{id}/`  | Detalhe de corrida        |
| PUT    | `/api/runs/{id}/`  | Atualizar corrida         |
| DELETE | `/api/runs/{id}/`  | Deletar corrida           |
| GET    | `/api/runs/stats/` | Estatísticas das corridas |

### Documentação

| Método | Endpoint       | Descrição             |
| ------ | -------------- | --------------------- |
| GET    | `/api/docs/`   | Documentação Swagger  |
| GET    | `/api/schema/` | Schema OpenAPI (JSON) |

## 🔐 Autenticação

A API usa **Token Authentication**. O login é feito com **email** (não username).

### Registro

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "senha_segura",
    "password_confirm": "senha_segura",
    "first_name": "Nome",
    "last_name": "Sobrenome"
  }'
```

Resposta:

```json
{
  "token": "abc123...",
  "email": "user@example.com",
  "first_name": "Nome",
  "last_name": "Sobrenome"
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "senha_segura"
  }'
```

Resposta:

```json
{
  "token": "abc123..."
}
```

### Mudar Senha

```bash
curl -X PUT http://localhost:8000/api/auth/change-password/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "senha_atual",
    "new_password": "nova_senha_segura",
    "new_password_confirm": "nova_senha_segura"
  }'
```

Resposta:

```json
{
  "message": "Senha alterada com sucesso.",
  "token": "novo_token_xyz..."
}
```

⚠️ **Importante:** Após mudar a senha, use o novo token retornado.

### Usando o Token

Adicione o token no header `Authorization` em todas as requisições autenticadas:

```bash
curl http://localhost:8000/api/runs/ \
  -H "Authorization: Token abc123..."
```

## 🏃 Exemplo de Uso

### Criar uma corrida

```bash
curl -X POST http://localhost:8000/api/runs/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-10T10:00:00Z",
    "distance_km": 5.0,
    "time_minutes": 30.0
  }'
```

### Listar corridas

```bash
curl http://localhost:8000/api/runs/ \
  -H "Authorization: Token abc123..."
```

### Ver estatísticas

```bash
curl http://localhost:8000/api/runs/stats/ \
  -H "Authorization: Token abc123..."
```

Resposta:

```json
{
  "total_runs": 10,
  "total_distance": 50.5,
  "avg_pace": 6.2,
  "best_pace": 5.8
}
```

## 🚀 Deploy no Render

### 1. Configure as variáveis de ambiente

No Render, adicione as seguintes variáveis:

```env
SECRET_KEY=<gere-uma-nova-chave-diferente>
DEBUG=False
DATABASE_URL=<url-do-neon-db>
ALLOWED_HOSTS=<seu-app>.onrender.com
CORS_ALLOWED_ORIGINS=<url-do-frontend>
```

⚠️ **IMPORTANTE:**

- **Gere uma nova `SECRET_KEY`** para produção (diferente da de desenvolvimento)
- **`DEBUG=False`** em produção (nunca `True`)
- Adicione o domínio real em `ALLOWED_HOSTS`
- Configure `CORS_ALLOWED_ORIGINS` com os domínios autorizados

### 2. Configure os comandos no Render

- **Build Command:** `python render_build.py`
- **Start Command:** `python render_start.py`

### 3. Deploy

O Render automaticamente:

- Instala o UV
- Sincroniza dependências com `uv sync`
- Executa migrações
- Coleta arquivos estáticos
- Inicia o servidor com Gunicorn

## 🔒 Segurança

### SECRET_KEY

A `SECRET_KEY` é usada pelo Django para:

- Assinar cookies de sessão
- Gerar tokens CSRF
- Criptografar dados sensíveis

**Boas práticas:**

- ✅ Nunca comitar no Git
- ✅ Usar chave diferente em dev e produção
- ✅ Manter longa e aleatória
- ❌ Nunca compartilhar publicamente

### Geração de SECRET_KEY

```bash
uv run python - << 'EOF'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
EOF
```

## 📝 Modelo de Dados

### Run (Corrida)

```python
{
  "id": "uuid",
  "date": "datetime",
  "distance_km": "decimal",
  "time_minutes": "decimal",
  "pace": "float (calculado)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

O campo `pace` é calculado automaticamente: `time_minutes / distance_km` (min/km)

## 🧪 Testes

Para testar a API localmente, acesse a documentação interativa:

**http://localhost:8000/api/docs/**

Lá você pode:

- Ver todos os endpoints
- Testar requisições
- Ver schemas de request/response
- Autenticar com token

## 📄 Licença

ISC
