# Sistema de Alocação de Professores

Este projeto implementa o backend de uma aplicação para alocação automática de professores em disciplinas, com suporte a:

- Importação de planilhas (CSV/XLSX) de professores e disciplinas
- Algoritmo de alocação por área, horário e carga horária
- Exportação de alocações em CSV ou XLSX (raw ou Base64)
- Documentação Swagger via **drf-yasg**

---

## Tecnologias

- Python 3.11 + Django 5.2
- Django REST Framework
- drf-yasg (Swagger/OpenAPI)
- Pandas (para leitura/exportação de planilhas)
- PostgreSQL (ou outro RDBMS suportado pelo Django)

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
   pip install pip-tools
   pip-compile requirements.in
   pip-compile requirements-dev.in
   pip install -r requirements.txt        # runtime
   pip install -r requirements-dev.txt    # dev/tools
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

- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **Redoc**: `http://127.0.0.1:8000/redoc/`
- **JSON/YAML**: `http://127.0.0.1:8000/swagger.json` ou `.yaml`

---

## Endpoints Principais

Prefixo: `/api/v1/`

---

# Documentação Completa da API

Consulte também [docs/api.md](docs/api.md) para o spec completo.

---

## Contribuição

- Abra issues ou PRs para melhorias
- Siga o style guide e escreva testes para novos recursos

---

_Qualquer dúvida, comente!_
