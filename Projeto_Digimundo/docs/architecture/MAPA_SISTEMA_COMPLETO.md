# 🗺️ MAPA COMPLETO DO SISTEMA CINEPROD

**Data:** 2025-10-21
**Versão:** 1.0
**Objetivo:** Documentação completa de TODOS os arquivos que serão criados

---

## 📁 ESTRUTURA DE DIRETÓRIOS

```
cineprod/
├── app.py                          # Aplicação Flask principal
├── config.py                       # Configurações do sistema
├── requirements.txt                # Dependências Python
├── .env.example                    # Exemplo de variáveis de ambiente
├── .gitignore                      # Arquivos ignorados pelo Git
├── README.md                       # Documentação do projeto
│
├── app/                            # Pacote principal da aplicação
│   ├── __init__.py                 # Inicializa Flask app
│   │
│   ├── models/                     # Modelos de banco de dados (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── crew.py
│   │   ├── equipment.py
│   │   ├── location.py
│   │   ├── script.py
│   │   ├── analysis.py
│   │   ├── mood_board.py
│   │   ├── task.py
│   │   ├── storyboard.py
│   │   ├── shotlist.py
│   │   ├── call_sheet.py
│   │   ├── budget.py
│   │   ├── schedule.py
│   │   └── document.py
│   │
│   ├── routes/                     # Rotas/Controllers (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── projects.py
│   │   ├── crew.py
│   │   ├── equipment.py
│   │   ├── locations.py
│   │   ├── scripts.py
│   │   ├── mood_boards.py
│   │   ├── tasks.py
│   │   ├── storyboards.py
│   │   ├── shotlists.py
│   │   ├── call_sheets.py
│   │   ├── budget.py
│   │   ├── schedule.py
│   │   ├── documents.py
│   │   └── api.py
│   │
│   ├── services/                   # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── pdf_parser.py
│   │   ├── llm_service.py
│   │   ├── breakdown_service.py
│   │   ├── export_service.py
│   │   └── scripturemon/          # Sistema de análise
│   │       ├── __init__.py
│   │       ├── analyzer.py
│   │       └── (copiar do scripturemon original)
│   │
│   ├── static/                     # Arquivos estáticos
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   ├── dashboard.css
│   │   │   ├── mood-board.css
│   │   │   ├── storyboard.css
│   │   │   └── kanban.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── mood-board.js
│   │   │   ├── tasks-kanban.js
│   │   │   ├── storyboard.js
│   │   │   ├── shotlist.js
│   │   │   └── calendar.js
│   │   ├── img/
│   │   │   └── logo.png
│   │   └── uploads/               # Arquivos enviados pelos usuários
│   │       ├── scripts/
│   │       ├── mood-boards/
│   │       ├── storyboards/
│   │       └── documents/
│   │
│   ├── templates/                  # Templates HTML (Jinja2)
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard/
│   │   │   └── index.html
│   │   ├── projects/
│   │   │   ├── index.html
│   │   │   ├── view.html
│   │   │   ├── create.html
│   │   │   └── edit.html
│   │   ├── crew/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   ├── equipment/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   ├── locations/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   ├── scripts/
│   │   │   ├── index.html
│   │   │   ├── upload.html
│   │   │   └── view.html
│   │   ├── mood_boards/
│   │   │   ├── index.html
│   │   │   ├── view.html
│   │   │   └── create.html
│   │   ├── tasks/
│   │   │   ├── index.html
│   │   │   ├── kanban.html
│   │   │   └── form.html
│   │   ├── storyboards/
│   │   │   ├── index.html
│   │   │   ├── view.html
│   │   │   └── create.html
│   │   ├── shotlists/
│   │   │   ├── index.html
│   │   │   ├── view.html
│   │   │   └── create.html
│   │   ├── call_sheets/
│   │   │   ├── index.html
│   │   │   └── view.html
│   │   ├── budget/
│   │   │   └── index.html
│   │   ├── schedule/
│   │   │   ├── index.html
│   │   │   └── calendar.html
│   │   └── components/
│   │       ├── navbar.html
│   │       ├── sidebar.html
│   │       └── modals.html
│   │
│   └── utils/                      # Funções utilitárias
│       ├── __init__.py
│       ├── decorators.py
│       ├── helpers.py
│       └── validators.py
│
├── migrations/                     # Migrations do banco (Flask-Migrate)
│   └── versions/
│
└── tests/                          # Testes
    ├── __init__.py
    ├── test_auth.py
    ├── test_projects.py
    └── test_services.py
```

---

## 📄 ARQUIVOS RAIZ

### `app.py`
**Propósito:** Ponto de entrada da aplicação Flask
**Função:** Inicia o servidor e registra blueprints
**Encaminhamentos:** Nenhum (arquivo principal)

```python
# Inicializa Flask app
# Configura banco de dados
# Registra blueprints (routes)
# Roda servidor em modo debug
```

### `config.py`
**Propósito:** Configurações centralizadas
**Função:** Define configurações de desenvolvimento/produção
**Encaminhamentos:** Usado por `app.py` e todos os módulos

```python
# DATABASE_URL
# SECRET_KEY
# UPLOAD_FOLDER
# MAX_FILE_SIZE
# OLLAMA_API_URL
```

### `requirements.txt`
**Propósito:** Dependências Python
**Função:** Lista todos os pacotes necessários

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Login==0.6.3
Flask-CORS==4.0.0
Werkzeug==3.0.1
PyPDF2==3.0.1
python-dotenv==1.0.0
requests==2.31.0
Pillow==10.1.0
```

### `.env.example`
**Propósito:** Template de variáveis de ambiente
**Função:** Mostra quais variáveis configurar

```
DATABASE_URL=sqlite:///cineprod.db
SECRET_KEY=your-secret-key-here
OLLAMA_API_URL=http://localhost:11434
OPENAI_API_KEY=optional
```

### `README.md`
**Propósito:** Documentação do projeto
**Função:** Instruções de instalação e uso

---

## 📦 APP/__INIT__.PY

**Propósito:** Inicializa a aplicação Flask
**Função:** Factory pattern para criar app
**Encaminhamentos:** Importa todos os blueprints

```python
# Cria app Flask
# Configura SQLAlchemy
# Configura Flask-Login
# Registra blueprints
# Cria tabelas no banco
```

---

## 🗄️ MODELS (app/models/)

### `user.py`
**Propósito:** Modelo de usuário
**Tabela:** `users`
**Campos:** id, email, password_hash, name, role, created_at
**Relações:**
- `projects` (1:N)
- `tasks` (1:N)
- `created_items` (polimórfico)

### `project.py`
**Propósito:** Modelo de projeto
**Tabela:** `projects`
**Campos:** id, name, type, status, director, producer, budget, start_date, end_date, description, user_id, created_at
**Relações:**
- `user` (N:1)
- `crew` (1:N)
- `scripts` (1:N)
- `mood_boards` (1:N)
- `tasks` (1:N)
- `storyboards` (1:N)
- `shotlists` (1:N)
- `call_sheets` (1:N)
- `budget_items` (1:N)
- `schedule_events` (1:N)

### `crew.py`
**Propósito:** Modelo de membro da equipe
**Tabela:** `crew`
**Campos:** id, name, role, department, email, phone, project_id, daily_rate, status, created_at
**Relações:**
- `project` (N:1)
- `tasks` (N:N através de `task_assignments`)

### `equipment.py`
**Propósito:** Modelo de equipamento
**Tabela:** `equipment`
**Campos:** id, name, category, brand, model, serial_number, status, daily_rate, location, created_at
**Relações:**
- `shotlist_items` (N:N)
- `reservations` (1:N)

### `location.py`
**Propósito:** Modelo de locação
**Tabela:** `locations`
**Campos:** id, name, type, address, capacity, daily_rate, status, contact, created_at
**Relações:**
- `schedule_events` (1:N)
- `call_sheets` (1:N)

### `script.py`
**Propósito:** Modelo de roteiro
**Tabela:** `scripts`
**Campos:** id, project_id, title, filename, file_path, text_content, uploaded_at, uploaded_by, status
**Relações:**
- `project` (N:1)
- `analyses` (1:N)

### `analysis.py`
**Propósito:** Modelo de análise do Scripturemon
**Tabela:** `script_analyses`
**Campos:** id, script_id, status, started_at, completed_at, total_specialists, completed_specialists, model_used, results_path
**Relações:**
- `script` (N:1)
- `specialist_results` (1:N)

**Sub-modelo:** `specialist_results`
**Tabela:** `specialist_results`
**Campos:** id, analysis_id, specialist_name, author_name, result_html, score, issues_found, created_at

### `mood_board.py`
**Propósito:** Modelos de mood board
**Tabela 1:** `mood_boards`
**Campos:** id, project_id, title, description, created_by, created_at
**Relações:**
- `project` (N:1)
- `items` (1:N)

**Tabela 2:** `mood_board_items`
**Campos:** id, mood_board_id, type, file_path, url, caption, position_x, position_y, created_at

### `task.py`
**Propósito:** Modelos de tarefas
**Tabela 1:** `tasks`
**Campos:** id, project_id, title, description, assigned_to, status, priority, due_date, completed_at, created_by, created_at
**Relações:**
- `project` (N:1)
- `assigned_user` (N:1)
- `comments` (1:N)

**Tabela 2:** `task_comments`
**Campos:** id, task_id, user_id, comment, created_at

### `storyboard.py`
**Propósito:** Modelos de storyboard
**Tabela 1:** `storyboards`
**Campos:** id, project_id, scene_number, scene_title, created_by, created_at
**Relações:**
- `project` (N:1)
- `frames` (1:N)

**Tabela 2:** `storyboard_frames`
**Campos:** id, storyboard_id, frame_number, image_path, description, camera_angle, movement, duration, dialogue, created_at

### `shotlist.py`
**Propósito:** Modelos de shotlist
**Tabela 1:** `shotlists`
**Campos:** id, project_id, scene_number, created_by, created_at
**Relações:**
- `project` (N:1)
- `items` (1:N)

**Tabela 2:** `shotlist_items`
**Campos:** id, shotlist_id, shot_number, shot_type, camera_angle, movement, lens, framing, duration, description, equipment_needed, notes, completed, created_at

### `call_sheet.py`
**Propósito:** Modelo de call sheet
**Tabela:** `call_sheets`
**Campos:** id, project_id, shoot_date, location_id, scenes, crew_list, equipment_list, notes, created_at
**Relações:**
- `project` (N:1)
- `location` (N:1)

### `budget.py`
**Propósito:** Modelo de orçamento
**Tabela:** `budget_items`
**Campos:** id, project_id, category, description, estimated, actual, status, created_at
**Relações:**
- `project` (N:1)

### `schedule.py`
**Propósito:** Modelo de cronograma
**Tabela:** `schedule_events`
**Campos:** id, project_id, title, start_date, end_date, type, location_id, notes, created_at
**Relações:**
- `project` (N:1)
- `location` (N:1)

### `document.py`
**Propósito:** Modelo de documento
**Tabela:** `documents`
**Campos:** id, project_id, name, type, file_path, uploaded_by, uploaded_at
**Relações:**
- `project` (N:1)

---

## 🛤️ ROUTES (app/routes/)

### `auth.py`
**Blueprint:** `auth`
**Prefix:** `/auth`
**Propósito:** Autenticação de usuários
**Rotas:**
- `GET /login` → Exibe formulário de login → Template: `auth/login.html`
- `POST /login` → Processa login → Service: `auth_service.authenticate()`
- `GET /register` → Exibe formulário de registro → Template: `auth/register.html`
- `POST /register` → Cria novo usuário → Service: `auth_service.create_user()`
- `GET /logout` → Faz logout → Redirect: `/auth/login`

### `dashboard.py`
**Blueprint:** `dashboard`
**Prefix:** `/`
**Propósito:** Dashboard principal
**Rotas:**
- `GET /` → Dashboard home → Template: `dashboard/index.html`

**Dados exibidos:**
- Total de projetos
- Projetos ativos
- Tasks pendentes
- Próximos eventos (calendar)
- Análises em andamento

### `projects.py`
**Blueprint:** `projects`
**Prefix:** `/projects`
**Propósito:** CRUD de projetos
**Rotas:**
- `GET /` → Lista todos projetos → Template: `projects/index.html`
- `GET /<id>` → Visualiza projeto → Template: `projects/view.html`
- `GET /create` → Formulário criar → Template: `projects/create.html`
- `POST /create` → Cria projeto → Redirect: `/projects/<id>`
- `GET /<id>/edit` → Formulário editar → Template: `projects/edit.html`
- `POST /<id>/edit` → Atualiza projeto → Redirect: `/projects/<id>`
- `POST /<id>/delete` → Deleta projeto → Redirect: `/projects`

### `crew.py`
**Blueprint:** `crew`
**Prefix:** `/crew`
**Propósito:** CRUD de equipe
**Rotas:**
- `GET /` → Lista equipe → Template: `crew/index.html`
- `GET /create` → Formulário → Template: `crew/form.html`
- `POST /create` → Cria membro → Redirect: `/crew`
- `GET /<id>/edit` → Formulário editar → Template: `crew/form.html`
- `POST /<id>/edit` → Atualiza → Redirect: `/crew`
- `POST /<id>/delete` → Deleta → Redirect: `/crew`

### `equipment.py`
**Blueprint:** `equipment`
**Prefix:** `/equipment`
**Propósito:** CRUD de equipamentos
**Rotas:**
- `GET /` → Lista equipamentos → Template: `equipment/index.html`
- `GET /create` → Formulário → Template: `equipment/form.html`
- `POST /create` → Cria equipamento → Redirect: `/equipment`
- `GET /<id>/edit` → Formulário editar → Template: `equipment/form.html`
- `POST /<id>/edit` → Atualiza → Redirect: `/equipment`
- `POST /<id>/delete` → Deleta → Redirect: `/equipment`

### `locations.py`
**Blueprint:** `locations`
**Prefix:** `/locations`
**Propósito:** CRUD de locações
**Rotas:**
- `GET /` → Lista locações → Template: `locations/index.html`
- `GET /create` → Formulário → Template: `locations/form.html`
- `POST /create` → Cria locação → Redirect: `/locations`
- `GET /<id>/edit` → Formulário editar → Template: `locations/form.html`
- `POST /<id>/edit` → Atualiza → Redirect: `/locations`
- `POST /<id>/delete` → Deleta → Redirect: `/locations`

### `scripts.py`
**Blueprint:** `scripts`
**Prefix:** `/scripts`
**Propósito:** Upload e visualização de roteiros
**Rotas:**
- `GET /` → Lista roteiros → Template: `scripts/index.html`
- `GET /upload` → Formulário upload → Template: `scripts/upload.html`
- `POST /upload` → Faz upload → Service: `pdf_parser.extract_text()`
- `GET /<id>` → Visualiza roteiro → Template: `scripts/view.html`
- `POST /<id>/analyze` → Inicia análise → Service: `scripturemon.analyzer.run()`
- `GET /<id>/analysis/<analysis_id>` → Ver análise → Template: `scripts/analysis.html`

### `mood_boards.py`
**Blueprint:** `mood_boards`
**Prefix:** `/mood-boards`
**Propósito:** CRUD de mood boards
**Rotas:**
- `GET /` → Lista mood boards → Template: `mood_boards/index.html`
- `GET /create` → Formulário → Template: `mood_boards/create.html`
- `POST /create` → Cria mood board → Redirect: `/mood-boards/<id>`
- `GET /<id>` → Visualiza mood board → Template: `mood_boards/view.html`
- `POST /<id>/add-item` → Adiciona item → Service: Upload de imagem
- `POST /<id>/items/<item_id>/move` → Move item (drag&drop) → JSON response
- `POST /<id>/items/<item_id>/delete` → Remove item → JSON response

### `tasks.py`
**Blueprint:** `tasks`
**Prefix:** `/tasks`
**Propósito:** CRUD de tasks
**Rotas:**
- `GET /` → Lista tasks → Template: `tasks/index.html`
- `GET /kanban` → View Kanban → Template: `tasks/kanban.html`
- `GET /create` → Formulário → Template: `tasks/form.html`
- `POST /create` → Cria task → Redirect: `/tasks`
- `POST /<id>/update-status` → Atualiza status (drag Kanban) → JSON response
- `POST /<id>/comment` → Adiciona comentário → JSON response
- `POST /<id>/delete` → Deleta → Redirect: `/tasks`

### `storyboards.py`
**Blueprint:** `storyboards`
**Prefix:** `/storyboards`
**Propósito:** CRUD de storyboards
**Rotas:**
- `GET /` → Lista storyboards → Template: `storyboards/index.html`
- `GET /create` → Formulário → Template: `storyboards/create.html`
- `POST /create` → Cria storyboard → Redirect: `/storyboards/<id>`
- `GET /<id>` → Visualiza storyboard → Template: `storyboards/view.html`
- `POST /<id>/add-frame` → Adiciona frame → Service: Upload de imagem
- `POST /<id>/frames/<frame_id>/edit` → Edita frame → JSON response
- `GET /<id>/export-pdf` → Exporta PDF → Service: `export_service.storyboard_to_pdf()`

### `shotlists.py`
**Blueprint:** `shotlists`
**Prefix:** `/shotlists`
**Propósito:** CRUD de shotlists
**Rotas:**
- `GET /` → Lista shotlists → Template: `shotlists/index.html`
- `GET /create` → Formulário → Template: `shotlists/create.html`
- `POST /create` → Cria shotlist → Redirect: `/shotlists/<id>`
- `GET /<id>` → Visualiza shotlist → Template: `shotlists/view.html`
- `POST /<id>/add-shot` → Adiciona shot → JSON response
- `POST /<id>/shots/<shot_id>/edit` → Edita shot → JSON response
- `POST /<id>/shots/<shot_id>/complete` → Marca como concluído → JSON response
- `GET /<id>/export-csv` → Exporta CSV → Service: `export_service.shotlist_to_csv()`

### `call_sheets.py`
**Blueprint:** `call_sheets`
**Prefix:** `/call-sheets`
**Propósito:** Geração e envio de call sheets
**Rotas:**
- `GET /` → Lista call sheets → Template: `call_sheets/index.html`
- `GET /create` → Formulário → Template: `call_sheets/create.html`
- `POST /create` → Cria call sheet → Service: `call_sheet_service.generate()`
- `GET /<id>` → Visualiza call sheet → Template: `call_sheets/view.html`
- `GET /<id>/pdf` → Exporta PDF → Service: `export_service.call_sheet_to_pdf()`
- `POST /<id>/send` → Envia por email → Service: `email_service.send_call_sheet()`

### `budget.py`
**Blueprint:** `budget`
**Prefix:** `/budget`
**Propósito:** Gerenciamento de orçamento
**Rotas:**
- `GET /` → Lista orçamentos → Template: `budget/index.html`
- `POST /add-item` → Adiciona item → JSON response
- `POST /items/<id>/edit` → Edita item → JSON response
- `POST /items/<id>/delete` → Remove item → JSON response

### `schedule.py`
**Blueprint:** `schedule`
**Prefix:** `/schedule`
**Propósito:** Cronograma/calendário
**Rotas:**
- `GET /` → View calendário → Template: `schedule/calendar.html`
- `GET /events` → Lista eventos (API JSON) → JSON response
- `POST /events/create` → Cria evento → JSON response
- `POST /events/<id>/edit` → Edita evento → JSON response
- `POST /events/<id>/delete` → Remove evento → JSON response

### `documents.py`
**Blueprint:** `documents`
**Prefix:** `/documents`
**Propósito:** Upload e gerenciamento de documentos
**Rotas:**
- `GET /` → Lista documentos → Template: `documents/index.html`
- `POST /upload` → Upload documento → Service: File upload
- `GET /<id>/download` → Download documento → Send file
- `POST /<id>/delete` → Remove documento → Redirect: `/documents`

### `api.py`
**Blueprint:** `api`
**Prefix:** `/api`
**Propósito:** API JSON para ações AJAX
**Rotas:**
- `POST /ai/breakdown` → IA faz breakdown do roteiro → JSON
- `POST /ai/generate-tasks` → IA gera tasks → JSON
- `POST /ai/suggest-shotlist` → IA sugere shotlist → JSON
- `POST /ai/optimize-schedule` → IA otimiza cronograma → JSON
- `POST /ai/chat` → Chat com IA → JSON

---

## ⚙️ SERVICES (app/services/)

### `auth_service.py`
**Propósito:** Lógica de autenticação
**Funções:**
- `authenticate(email, password)` → Valida login
- `create_user(email, password, name, role)` → Cria usuário
- `hash_password(password)` → Hash senha
- `verify_password(hash, password)` → Verifica senha

### `pdf_parser.py`
**Propósito:** Extração de texto de PDF
**Funções:**
- `extract_text(pdf_path)` → Extrai texto do roteiro PDF
- `parse_scenes(text)` → Identifica cenas no roteiro
- `extract_dialogues(text)` → Extrai diálogos

### `llm_service.py`
**Propósito:** Comunicação com LLMs
**Funções:**
- `call_ollama(prompt, model)` → Chama Ollama API
- `call_openai(prompt, model)` → Chama OpenAI API (opcional)
- `stream_response(prompt)` → Stream de resposta

### `breakdown_service.py`
**Propósito:** Breakdown automático de roteiro
**Funções:**
- `extract_equipment(script_text)` → IA identifica equipamentos
- `extract_locations(script_text)` → IA identifica locações
- `extract_characters(script_text)` → IA identifica personagens
- `generate_tasks(script_text)` → IA gera tasks de pré-produção

### `export_service.py`
**Propósito:** Exportação para PDF/CSV
**Funções:**
- `storyboard_to_pdf(storyboard_id)` → Exporta storyboard
- `shotlist_to_csv(shotlist_id)` → Exporta shotlist
- `call_sheet_to_pdf(call_sheet_id)` → Exporta call sheet

### `scripturemon/analyzer.py`
**Propósito:** Integração com Scripturemon
**Funções:**
- `analyze_script(script_id)` → Inicia análise dos 24 especialistas
- `get_analysis_status(analysis_id)` → Status da análise
- `get_results(analysis_id)` → Resultados da análise

---

## 🎨 TEMPLATES (app/templates/)

### `base.html`
**Propósito:** Template base (herança)
**Blocos:**
- `{% block title %}`
- `{% block head %}` → CSS customizado
- `{% block content %}` → Conteúdo principal
- `{% block scripts %}` → JS customizado

**Inclui:**
- `components/navbar.html`
- `components/sidebar.html`

### `auth/login.html`
**Extends:** `base.html`
**Formulário:**
- Email (input)
- Senha (input)
- Botão "Entrar"
- Link "Registrar"

**Encaminhamentos:**
- POST → `/auth/login`
- Link → `/auth/register`

### `auth/register.html`
**Extends:** `base.html`
**Formulário:**
- Nome (input)
- Email (input)
- Senha (input)
- Confirmar senha (input)
- Botão "Criar Conta"

**Encaminhamentos:**
- POST → `/auth/register`

### `dashboard/index.html`
**Extends:** `base.html`
**Seções:**
- Cards de estatísticas (projetos, tasks, eventos)
- Lista de projetos recentes
- Tasks pendentes
- Próximos eventos do calendário

**Encaminhamentos:**
- Links → `/projects`, `/tasks`, `/schedule`

### `projects/index.html`
**Extends:** `base.html`
**Seções:**
- Botão "Novo Projeto"
- Tabela de projetos (nome, tipo, status, datas)
- Ações (ver, editar, deletar)

**Encaminhamentos:**
- Link → `/projects/create`
- Links → `/projects/<id>`

### `projects/view.html`
**Extends:** `base.html`
**Seções:**
- Informações do projeto
- Tabs:
  - Roteiros
  - Mood Boards
  - Storyboards
  - Shotlists
  - Tasks
  - Equipe
  - Orçamento

**Encaminhamentos:**
- Links para módulos relacionados

### `projects/create.html` e `projects/edit.html`
**Extends:** `base.html`
**Formulário:**
- Nome, tipo, status, diretor, produtor, orçamento, datas, descrição

**Encaminhamentos:**
- POST → `/projects/create` ou `/projects/<id>/edit`

### `mood_boards/view.html`
**Extends:** `base.html`
**Seções:**
- Grid de imagens (drag & drop)
- Botão "Adicionar Item"
- Modal de upload

**JavaScript:**
- `static/js/mood-board.js` (drag & drop)

**Encaminhamentos:**
- POST → `/mood-boards/<id>/add-item`
- POST → `/mood-boards/<id>/items/<item_id>/move`

### `tasks/kanban.html`
**Extends:** `base.html`
**Seções:**
- 4 colunas: To Do, In Progress, Review, Done
- Cards de tasks (drag & drop)
- Botão "Nova Task"

**JavaScript:**
- `static/js/tasks-kanban.js` (drag & drop)

**Encaminhamentos:**
- POST → `/tasks/<id>/update-status`

### `storyboards/view.html`
**Extends:** `base.html`
**Seções:**
- Grid de frames
- Formulário adicionar frame
- Campos técnicos (ângulo, movimento, duração)

**JavaScript:**
- `static/js/storyboard.js`

**Encaminhamentos:**
- POST → `/storyboards/<id>/add-frame`

### `shotlists/view.html`
**Extends:** `base.html`
**Seções:**
- Tabela de shots
- Campos: número, tipo, ângulo, lente, duração, equipamentos
- Checkbox "concluído"

**JavaScript:**
- `static/js/shotlist.js`

**Encaminhamentos:**
- POST → `/shotlists/<id>/add-shot`
- POST → `/shotlists/<id>/shots/<shot_id>/complete`

### `schedule/calendar.html`
**Extends:** `base.html`
**Seções:**
- Calendário interativo (FullCalendar.js)
- Modal criar evento

**JavaScript:**
- `static/js/calendar.js`
- Library: FullCalendar

**Encaminhamentos:**
- GET → `/schedule/events` (JSON)
- POST → `/schedule/events/create`

### `components/navbar.html`
**Propósito:** Barra superior
**Elementos:**
- Logo
- Busca
- Notificações
- User menu (logout)

### `components/sidebar.html`
**Propósito:** Menu lateral
**Links:**
- Dashboard
- Projetos
- Roteiros
- Mood Boards
- Tasks
- Storyboards
- Shotlists
- Call Sheets
- Equipe
- Equipamentos
- Locações
- Orçamento
- Cronograma
- Documentos

---

## 🎨 STATIC FILES

### CSS

**`static/css/main.css`**
- Estilos globais
- Variáveis CSS (cores do StudioBinder)
- Typography
- Buttons
- Forms
- Cards
- Tables

**`static/css/dashboard.css`**
- Grid de cards
- Estatísticas
- Layout dashboard

**`static/css/mood-board.css`**
- Grid de imagens
- Drag & drop visual
- Modal de upload

**`static/css/storyboard.css`**
- Grid de frames
- Cards de frame

**`static/css/kanban.css`**
- Colunas Kanban
- Cards de task
- Drag & drop

### JavaScript

**`static/js/main.js`**
- Funções globais
- AJAX helpers
- Modals
- Alerts

**`static/js/mood-board.js`**
- Drag & drop de imagens
- Upload de arquivos
- Reordenação de grid

**`static/js/tasks-kanban.js`**
- Drag & drop entre colunas
- Atualização de status

**`static/js/storyboard.js`**
- Upload de frames
- Edição inline
- Reordenação

**`static/js/shotlist.js`**
- Adicionar shots
- Edição inline
- Marcar concluído

**`static/js/calendar.js`**
- Integração FullCalendar
- Criar/editar eventos
- Arrastar eventos

---

## 🧪 TESTS

### `test_auth.py`
- `test_register()`
- `test_login()`
- `test_logout()`
- `test_login_invalid()`

### `test_projects.py`
- `test_create_project()`
- `test_edit_project()`
- `test_delete_project()`
- `test_view_project()`

### `test_services.py`
- `test_pdf_parser()`
- `test_breakdown_service()`
- `test_llm_service()`

---

## 🔄 FLUXO DE DADOS ENTRE ARQUIVOS

### Exemplo: Upload de Roteiro

```
1. User acessa /scripts/upload
   → routes/scripts.py: upload_page()
   → templates/scripts/upload.html

2. User faz upload do PDF
   → POST /scripts/upload
   → routes/scripts.py: upload_script()
   → services/pdf_parser.py: extract_text()
   → models/script.py: Script.create()
   → Salva em: static/uploads/scripts/

3. User clica "Analisar"
   → POST /scripts/<id>/analyze
   → routes/scripts.py: analyze_script()
   → services/scripturemon/analyzer.py: analyze_script()
   → models/analysis.py: Analysis.create()
   → Salva resultados em DB

4. User vê resultados
   → GET /scripts/<id>/analysis/<analysis_id>
   → routes/scripts.py: view_analysis()
   → templates/scripts/analysis.html
```

### Exemplo: Mood Board com IA

```
1. User cria Mood Board
   → POST /mood-boards/create
   → routes/mood_boards.py: create()
   → models/mood_board.py: MoodBoard.create()

2. User adiciona imagem
   → POST /mood-boards/<id>/add-item
   → routes/mood_boards.py: add_item()
   → Salva em: static/uploads/mood-boards/
   → models/mood_board.py: MoodBoardItem.create()

3. User clica "IA: Analisar Paleta"
   → POST /api/ai/analyze-palette
   → routes/api.py: analyze_palette()
   → services/llm_service.py: call_ollama()
   → Retorna JSON com paleta de cores
```

### Exemplo: Kanban de Tasks

```
1. User acessa Kanban
   → GET /tasks/kanban
   → routes/tasks.py: kanban()
   → templates/tasks/kanban.html
   → JS: static/js/tasks-kanban.js

2. User arrasta task
   → JS detecta drag & drop
   → POST /tasks/<id>/update-status
   → routes/tasks.py: update_status()
   → models/task.py: Task.update()
   → Retorna JSON success

3. Interface atualiza
   → JS recebe resposta
   → Move card visualmente
```

---

## 📦 DEPENDÊNCIAS ENTRE ARQUIVOS

### Models dependem de:
- `app/__init__.py` (db instance)
- `config.py` (configurações)

### Routes dependem de:
- `models/*` (acesso aos dados)
- `services/*` (lógica de negócio)
- `templates/*` (renderização)
- `utils/decorators.py` (`@login_required`)

### Services dependem de:
- `models/*` (manipulação de dados)
- `config.py` (configurações)

### Templates dependem de:
- `static/css/*` (estilos)
- `static/js/*` (interatividade)
- `components/*` (partes reutilizáveis)

---

## 🎯 ORDEM DE CRIAÇÃO RECOMENDADA

### FASE 1: Setup (Dia 1)
1. `config.py`
2. `requirements.txt`
3. `.env.example`
4. `app.py`
5. `app/__init__.py`

### FASE 2: Auth & Dashboard (Dia 2-3)
6. `app/models/user.py`
7. `app/routes/auth.py`
8. `app/services/auth_service.py`
9. `app/templates/base.html`
10. `app/templates/components/navbar.html`
11. `app/templates/components/sidebar.html`
12. `app/templates/auth/login.html`
13. `app/templates/auth/register.html`
14. `app/templates/dashboard/index.html`
15. `app/routes/dashboard.py`
16. `app/static/css/main.css`

### FASE 3: Projetos (Dia 4-5)
17. `app/models/project.py`
18. `app/routes/projects.py`
19. `app/templates/projects/*` (4 arquivos)

### FASE 4: CRUD Básico (Dia 6-8)
20. `app/models/crew.py`
21. `app/routes/crew.py`
22. `app/templates/crew/*`
23. (Repetir para equipment, locations, budget, documents)

### FASE 5: Roteiros & Scripturemon (Dia 9-11)
24. `app/models/script.py`
25. `app/models/analysis.py`
26. `app/services/pdf_parser.py`
27. `app/services/scripturemon/` (copiar do original)
28. `app/routes/scripts.py`
29. `app/templates/scripts/*`

### FASE 6: Módulos Criativos (Dia 12-18)
30. Mood Boards (models + routes + templates + JS)
31. Tasks (models + routes + templates + Kanban JS)
32. Storyboards (models + routes + templates + JS)
33. Shotlists (models + routes + templates + JS)
34. Calendar (routes + templates + FullCalendar)

### FASE 7: Call Sheets (Dia 19-20)
35. `app/models/call_sheet.py`
36. `app/routes/call_sheets.py`
37. `app/services/export_service.py`
38. `app/templates/call_sheets/*`

### FASE 8: IA Multi-funcional (Dia 21-25)
39. `app/services/llm_service.py`
40. `app/services/breakdown_service.py`
41. `app/routes/api.py`
42. Integrar IA em mood_boards, tasks, storyboards, shotlists

### FASE 9: Polish & Tests (Dia 26-30)
43. `tests/*`
44. `README.md`
45. Ajustes finais CSS/JS
46. Deploy local completo

---

## ✅ CHECKLIST DE COMPLETUDE

Quando ESTE arquivo estiver completo, você terá:

- [ ] 📄 14 arquivos de models
- [ ] 🛤️ 14 arquivos de routes
- [ ] 🎨 30+ arquivos de templates
- [ ] ⚙️ 6 arquivos de services
- [ ] 🎨 10 arquivos CSS/JS
- [ ] 🧪 3+ arquivos de testes
- [ ] 📦 5 arquivos raiz (config, app, requirements, etc.)

**Total:** ~80+ arquivos organizados e documentados

---

**Próximo passo:** Começar a criar os arquivos seguindo a ordem recomendada!

**Estimativa:** 30 dias para MVP completo funcionando localmente.

Depois disso, deploy no VPS será apenas configuração de servidor! 🚀
