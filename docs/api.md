```bash
BASE="http://localhost:8000/api/v1"
```

---

### 1. Alocações

```bash
# Listar todas as alocações
curl -X GET "$BASE/alocacoes/" \
     -H "Accept: application/json"

# Disparar alocação automática
curl -X POST "$BASE/alocacoes/auto/"

# Ler uma alocação específica
curl -X GET "$BASE/alocacoes/UUID_DA_ALOCACAO/"
```

---

### 2. Dashboard

```bash
# Resumo de contadores para o dashboard
curl -X GET "$BASE/dashboard/summary/" \
     -H "Accept: application/json"
```

---

### 3. Disciplinas

```bash
# Listar disciplinas
curl -X GET "$BASE/disciplinas/" \
     -H "Accept: application/json"

# Criar disciplina
curl -X POST "$BASE/disciplinas/" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Nova Disciplina",
       "area": "Matemática"
     }'

# Ler uma disciplina
curl -X GET "$BASE/disciplinas/UUID_DA_DISCIPLINA/"

# Atualizar totalmente (PUT)
curl -X PUT "$BASE/disciplinas/UUID_DA_DISCIPLINA/" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Disciplina Atualizada",
       "area": "Física"
     }'

# Atualização parcial (PATCH)
curl -X PATCH "$BASE/disciplinas/UUID_DA_DISCIPLINA/" \
     -H "Content-Type: application/json" \
     -d '{"area": "Química"}'

# Deletar disciplina
curl -X DELETE "$BASE/disciplinas/UUID_DA_DISCIPLINA/"
```

---

### 4. Importações

```bash
curl -X POST "$BASE/importacoes/" \
     -F "file=@/caminho/para/arquivo.csv"
```

---

### 5. Professores

```bash
# Listar professores
curl -X GET "$BASE/professores/" \
     -H "Accept: application/json"

# Criar professor
curl -X POST "$BASE/professores/" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Professor Exemplo",
       "areas": ["Matemática","Física"],
       "carga_horaria_maxima_semanal": 20
     }'

# Ler professor
curl -X GET "$BASE/professores/UUID_DO_PROFESSOR/"

# Atualizar totalmente (PUT)
curl -X PUT "$BASE/professores/UUID_DO_PROFESSOR/" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Nome Atualizado",
       "areas": [],
       "carga_horaria_maxima_semanal": 15
     }'

# Atualização parcial (PATCH)
curl -X PATCH "$BASE/professores/UUID_DO_PROFESSOR/" \
     -H "Content-Type: application/json" \
     -d '{"carga_horaria_maxima_semanal": 18}'

# Deletar professor
curl -X DELETE "$BASE/professores/UUID_DO_PROFESSOR/"
```

---

### 6. Turmas

```bash
# Listar turmas
curl -X GET "$BASE/turmas/" \
     -H "Accept: application/json"

# Criar turma
curl -X POST "$BASE/turmas/" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Turma X",
       "disciplina_id": "UUID_DA_DISCIPLINA",
       "dia_semana": "segunda",
       "horario_inicio": "08:00:00",
       "horario_fim": "10:00:00"
     }'

# Ler turma
curl -X GET "$BASE/turmas/UUID_DA_TURMA/"

# Atualizar totalmente (PUT)
curl -X PUT "$BASE/turmas/UUID_DA_TURMA/" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Turma Y",
       "disciplina_id": "OUTRO_UUID",
       "local": "Porto Alegre",
       "dia_semana": "terca",
       "horario_inicio": "14:00:00",
       "horario_fim": "16:00:00"
     }'

# Atualização parcial (PATCH)
curl -X PATCH "$BASE/turmas/UUID_DA_TURMA/" \
     -H "Content-Type: application/json" \
     -d '{"dia_semana": "quarta"}'

# Deletar turma
curl -X DELETE "$BASE/turmas/UUID_DA_TURMA/"
```
