# Sistema de Alocação de Professores

Este projeto implementa o backend de uma aplicação para alocação automática de professores em disciplinas, com suporte a:

* Importação de planilhas (CSV/XLSX) de professores e disciplinas
* Algoritmo de alocação por área, horário e carga horária
* Exportação de alocações em CSV ou XLSX (raw ou Base64)
* Documentação Swagger via **drf-yasg**

---

## Tecnologias

* Python 3.11 + Django 5.2
* Django REST Framework
* drf-yasg (Swagger/OpenAPI)
* Pandas (para leitura/exportação de planilhas)
* PostgreSQL (ou outro RDBMS suportado pelo Django)

---

## Estrutura do Projeto

```bash
alocacao_backend/         # Projeto Django
├── core/                 # App principal
│   ├── api/              # Views, serializers, urls
│   ├── models/           # Models de Professor, Disciplina, Alocacao, Importacao
│   └── services/         # Lógica de importação e alocação
├── alocacao_backend/     # Configurações do projeto
│   ├── settings.py       # Configurações gerais, TIME_ZONE=UTC, USE_TZ=True
│   ├── urls.py           # URLs principais (incluindo export estático)
│   └── wsgi.py
└── manage.py
```

---

## Instalação

1. Clone o repositório:

   ```bash
   git clone <repo_url>
   cd alocacao_backend
   ```

2. Crie e ative um virtualenv:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o `.env` (variáveis de banco, secret key, etc.)

5. Aplique migrações:

   ```bash
   python manage.py migrate
   ```

6. (Opcional) Crie um superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

---

## Documentação da API

* **Swagger UI**:  `http://127.0.0.1:8000/swagger/`
* **Redoc**:       `http://127.0.0.1:8000/redoc/`
* **JSON/YAML**:   `http://127.0.0.1:8000/swagger.json` ou `.yaml`

---

## Endpoints Principais

Prefixo: `/api/v1/`

### Autenticação (JWT)

```bash
POST /auth/token/        # obter tokens
auth/token/refresh/     # renovar access
```

### Professores

```bash
GET  /professores/       # listar
POST /professores/       # criar
GET  /professores/{id}/  # detalhes
PUT/PATCH/DELETE idem
```

### Disciplinas e Indisponibilidades

Mesmas operações em `/disciplinas/` e `/indisponibilidades/`.

### Importação em Lote

```bash
POST   /importacoes/        # upload CSV/XLSX de professores ou disciplinas
GET    /importacoes/{id}/   # status do job
GET    /importacoes/        # listar jobs
```

### Alocação

```bash
POST   /alocacoes/auto/     # dispara alocação automática
GET    /alocacoes/          # lista alocações geradas
```

### Exportação de Alocações

#### CSV

```bash
# Raw
GET  /alocacoes/export/csv/  # download CSV
# Base64
GET  /alocacoes/export/csv/?as_base64=1
```

#### XLSX

```bash
# Raw
GET  /alocacoes/export/xlsx/ # download Excel
# Base64
GET  /alocacoes/export/xlsx/?as_base64=1
```

---

## Fluxos Principais

### 1. Importação

1. Faz upload de planilha via `/importacoes/`
2. Backend valida todas as linhas (tudo ou nada)
3. Salva em transação atômica ou retorna lista de erros por linha

### 2. Alocação Automática

1. Consulta disciplinas sem alocação
2. Carrega todos os professores com carga atual (Aggregate + Coalesce)
3. Para cada disciplina:

   * Filtra por área, disponibilidade e carga restante
   * Balanceia por menor carga
   * Cria registro de Alocacao (com ou sem conflito)

### 3. Exportação

* View Django pura retorna `HttpResponse` com CSV/XLSX "raw", ou JSON Base64

---

## Timezone e Datas

* **Armazenamento em UTC** (settings: `USE_TZ=True`, `TIME_ZONE='UTC'`)
* Serialização em ISO8601 com sufixo `Z`
* Converta para o fuso do usuário no front-end via bibliotecas de data

---

## Contribuição

* Abra issues ou PRs para melhorias
* Siga o style guide e escreva testes para novos recursos

---

*Qualquer dúvida, comente!*
