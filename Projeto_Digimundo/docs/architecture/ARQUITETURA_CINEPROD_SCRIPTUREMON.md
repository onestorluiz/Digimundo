# 🎬 ARQUITETURA COMPLETA: CineProd + Scripturemon VPS

**Data:** 2025-10-21
**Objetivo:** Sistema integrado de gestão de produção cinematográfica com IA
**Deploy:** VPS Online

---

## 🎯 VISÃO GERAL

Sistema web completo que une:
- **CineProd:** Gestão de produção (projetos, equipe, equipamentos, orçamento, cronograma)
- **Scripturemon:** Análise de roteiros com 24 especialistas
- **Ferramentas Criativas:** Mood Board, Storyboard, Shotlist, Tasks
- **LLM Multi-funcional:** IA integrada em diversos módulos

**Benefícios:**
- ✅ Acesso remoto (qualquer lugar, qualquer dispositivo)
- ✅ LLM rodando no servidor (não depende do computador local)
- ✅ Equipe colaborando em tempo real
- ✅ Dados centralizados e seguros
- ✅ Escalável para crescimento

---

## 🏗️ ARQUITETURA TÉCNICA

### Stack Tecnológico

```
Frontend:
- HTML5 + CSS3
- JavaScript (Vanilla ou Vue.js para reatividade)
- Bootstrap ou Tailwind (UI components)

Backend:
- Python 3.13
- Flask (web framework)
- SQLAlchemy (ORM)
- PostgreSQL (banco de dados)
- Redis (cache/sessões)

LLM:
- Ollama (rodando no VPS)
- OpenAI API (backup/modelos específicos)

Deploy:
- Nginx (reverse proxy)
- Gunicorn (WSGI server)
- Supervisor (process manager)
- SSL/HTTPS (Let's Encrypt)
```

### Estrutura de Pastas

```
cineprod-system/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/               # Modelos de banco de dados
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── crew.py
│   │   ├── equipment.py
│   │   ├── location.py
│   │   ├── script.py
│   │   ├── analysis.py
│   │   └── ...
│   ├── routes/               # APIs e páginas
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── crew.py
│   │   ├── scripts.py
│   │   ├── analysis.py
│   │   └── ai_assistant.py
│   ├── services/             # Lógica de negócio
│   │   ├── scripturemon/     # Sistema de análise
│   │   │   ├── core_1_specialists/
│   │   │   ├── core_2_examples/
│   │   │   ├── core_3_llm/
│   │   │   └── analyzer.py
│   │   ├── llm_service.py    # Comunicação com LLMs
│   │   ├── pdf_parser.py     # Extração de roteiros
│   │   └── ai_helpers.py     # Outras funções IA
│   ├── static/               # Arquivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   └── templates/            # HTML templates
│       ├── base.html
│       ├── dashboard.html
│       ├── projects/
│       ├── scripts/
│       └── analysis/
├── migrations/               # Migrations do banco
├── tests/
├── requirements.txt
├── config.py
└── run.py
```

---

## 📊 BANCO DE DADOS

### Schema Principal

```sql
-- Usuários e Autenticação
users (id, email, password_hash, name, role, created_at)

-- Projetos
projects (id, name, type, status, director, producer, budget,
          start_date, end_date, description, user_id, created_at)

-- Equipe
crew (id, name, role, department, email, phone, project_id,
      daily_rate, status, created_at)

-- Equipamentos
equipment (id, name, category, brand, model, serial_number,
           status, daily_rate, location, created_at)

-- Locações
locations (id, name, type, address, capacity, daily_rate,
           status, contact, created_at)

-- Roteiros
scripts (id, project_id, title, filename, file_path, uploaded_at,
         uploaded_by, status)

-- Análises do Scripturemon
script_analyses (id, script_id, status, started_at, completed_at,
                 total_specialists, completed_specialists,
                 model_used, results_path)

specialist_results (id, analysis_id, specialist_name, author_name,
                   result_html, score, issues_found, created_at)

-- Call Sheets
call_sheets (id, project_id, shoot_date, location_id, scenes,
             crew_list, equipment_list, notes, created_at)

-- Orçamento
budget_items (id, project_id, category, description, estimated,
              actual, status, created_at)

-- Cronograma
schedule_events (id, project_id, title, start_date, end_date,
                type, location, notes, created_at)

-- Documentos
documents (id, project_id, name, type, file_path, uploaded_by,
           uploaded_at)

-- Mood Boards
mood_boards (id, project_id, title, description, created_by, created_at)

mood_board_items (id, mood_board_id, type, file_path, url, caption,
                  position_x, position_y, created_at)

-- Tasks
tasks (id, project_id, title, description, assigned_to, status,
       priority, due_date, completed_at, created_by, created_at)

task_comments (id, task_id, user_id, comment, created_at)

-- Storyboards
storyboards (id, project_id, scene_number, scene_title, created_by, created_at)

storyboard_frames (id, storyboard_id, frame_number, image_path,
                   description, camera_angle, movement, duration,
                   dialogue, created_at)

-- Shotlists
shotlists (id, project_id, scene_number, created_by, created_at)

shotlist_items (id, shotlist_id, shot_number, shot_type, camera_angle,
                movement, lens, framing, duration, description,
                equipment_needed, notes, created_at)

-- Conversas com IA
ai_conversations (id, user_id, context_type, context_id,
                  messages_json, created_at)
```

---

## 🤖 INTEGRAÇÕES LLM PLANEJADAS

### 1. **Análise de Roteiro (Scripturemon)**
- 24 especialistas analisando roteiro
- Relatórios HTML detalhados
- Scores e recomendações

### 2. **Assistente de Breakdown**
- IA lê roteiro e sugere:
  - Lista de equipamentos necessários
  - Locações identificadas
  - Personagens e figurantes
  - Props e cenografia
  - Efeitos especiais

### 3. **Gerador de Call Sheet**
- IA organiza:
  - Cenas do dia
  - Convocação de equipe
  - Lista de equipamentos
  - Logística

### 4. **Assistente de Orçamento**
- IA sugere custos baseado em:
  - Tipo de produção
  - Duração
  - Equipamentos
  - Equipe
  - Histórico de projetos anteriores

### 5. **Assistente de Cronograma**
- IA otimiza calendário considerando:
  - Disponibilidade de equipe
  - Locações
  - Complexidade das cenas
  - Budget de tempo

### 6. **Chat Inteligente de Produção**
- "Quantos dias de filmagem faltam?"
- "Qual o status do projeto X?"
- "Mostre equipamentos disponíveis para semana que vem"
- "Gere relatório de progresso"

### 7. **Análise de Diálogos**
- Extrai todos os diálogos do roteiro
- Analisa naturalidade
- Sugere melhorias

### 8. **Comparador de Versões**
- Compara versões de roteiro
- Mostra mudanças
- Análise de impacto nas análises

---

## 🎨 MÓDULOS CRIATIVOS (Inspirados em StudioBinder)

### 📌 1. **Mood Board**

**Funcionalidades:**
- Criar quadros visuais por projeto/cena
- Upload de imagens de referência (Pinterest-style)
- Adicionar URLs de vídeos, sites, fotos
- Arrastar e organizar elementos
- Compartilhar com equipe
- Comentários em cada item

**Integrações IA:**
- **Análise de Mood:** IA analisa imagens e sugere paleta de cores
- **Busca Inteligente:** "Encontre referências de filme noir anos 50"
- **Gerador de Mood:** IA cria mood board baseado no roteiro
- **Sugestões de Referências:** "Filmes similares ao seu conceito"
- **Extração de Estilo:** IA identifica estilos artísticos das imagens

**Schema:**
```sql
mood_boards (
    id, project_id, title, description,
    created_by, created_at
)

mood_board_items (
    id, mood_board_id, type, file_path, url,
    caption, position_x, position_y, created_at
)
```

---

### ✅ 2. **Tasks (Gerenciamento de Tarefas)**

**Funcionalidades:**
- Criar tasks por projeto
- Atribuir responsáveis
- Definir prioridades (Baixa, Média, Alta, Urgente)
- Status (To Do, In Progress, Review, Done)
- Datas de vencimento
- Comentários e anexos
- Filtros e busca avançada
- Kanban board view

**Integrações IA:**
- **Gerador de Tasks:** IA lê roteiro e sugere tasks de pré-produção
  - "Contratar figurinista para cena 12"
  - "Conseguir autorização para locação externa"
- **Priorização Inteligente:** IA ordena tasks por urgência real
- **Sugestão de Prazos:** Baseado em histórico de projetos similares
- **Detecção de Dependências:** "Task X depende de Y estar concluída"
- **Alertas Proativos:** "Tasks atrasadas que impactam cronograma"

**Schema:**
```sql
tasks (
    id, project_id, title, description,
    assigned_to, status, priority, due_date,
    completed_at, created_by, created_at
)

task_comments (
    id, task_id, user_id, comment, created_at
)
```

---

### 📅 3. **Calendar (Calendário de Produção)**

**Funcionalidades:**
- Visualização mensal/semanal/diária
- Eventos de produção (filmagens, reuniões, ensaios)
- Integração com call sheets
- Disponibilidade de equipe/equipamentos
- Exportar para Google Calendar
- Alertas e notificações
- Bloqueio de conflitos

**Integrações IA:**
- **Otimização de Cronograma:**
  - IA sugere melhor ordem de filmagem
  - Minimiza deslocamentos entre locações
  - Agrupa cenas por locação/elenco
- **Detecção de Conflitos:** "Câmera A ocupada em 2 eventos no mesmo dia"
- **Sugestão de Buffer:** IA adiciona tempo extra em cenas complexas
- **Previsão de Atrasos:** Baseado em histórico, alerta riscos
- **Ajuste Inteligente:** "Cena 10 atrasou, reorganizar próximos 3 dias"

**Integração:**
- Usa tabela `schedule_events` existente
- Adicionar campos: `recurrence`, `google_calendar_id`, `alert_minutes`

---

### 🎬 4. **Storyboard**

**Funcionalidades:**
- Criar storyboards por cena
- Upload de desenhos/imagens
- Ferramentas de desenho básicas (futuro)
- Descrição de cada quadro
- Informações técnicas:
  - Ângulo de câmera (Wide, Close-up, etc.)
  - Movimento (Pan, Tilt, Dolly, etc.)
  - Duração estimada
  - Diálogos/áudio
- Exportar PDF
- Compartilhar com DP e diretor

**Integrações IA:**
- **Gerador de Storyboard:**
  - IA lê roteiro e sugere composições visuais
  - "Cena 5: 4 quadros sugeridos"
- **Análise de Continuidade:** Detecta erros de continuidade visual
- **Sugestão de Ângulos:** Baseado em teoria cinematográfica
- **Estimativa de Tempo:** IA calcula duração de cena baseado em storyboard
- **Geração de Imagens (futuro):** IA gera concept art automático
- **Comparação com Referências:** "Similar a cena X de Blade Runner"

**Schema:**
```sql
storyboards (
    id, project_id, scene_number, scene_title,
    created_by, created_at
)

storyboard_frames (
    id, storyboard_id, frame_number, image_path,
    description, camera_angle, movement, duration,
    dialogue, created_at
)
```

---

### 🎥 5. **Shotlist (Lista de Planos)**

**Funcionalidades:**
- Lista detalhada de todos os planos
- Informações por take:
  - Número do shot
  - Tipo de plano (Establishing, Close-up, POV, etc.)
  - Ângulo de câmera
  - Movimento de câmera
  - Lente (24mm, 50mm, etc.)
  - Enquadramento
  - Duração
  - Equipamentos necessários
  - Notas especiais
- Reordenar por prioridade
- Marcar como concluído
- Exportar para call sheet

**Integrações IA:**
- **Gerador Automático de Shotlist:**
  - IA lê storyboard e roteiro
  - Sugere planos necessários por cena
  - "Cena 7 precisa de 8 planos para cobertura completa"
- **Otimização de Filmagem:**
  - Agrupa planos por setup de câmera
  - Minimiza mudanças de lente/equipamento
- **Sugestão de Equipamentos:**
  - "Plano 15 precisa: Dolly, 35mm, Steadicam"
- **Cálculo de Tempo:**
  - Estima tempo necessário por plano
  - "Esta shotlist = 6 horas de filmagem"
- **Detecção de Falta:** "Você esqueceu plano reverso na cena 3"

**Schema:**
```sql
shotlists (
    id, project_id, scene_number,
    created_by, created_at
)

shotlist_items (
    id, shotlist_id, shot_number, shot_type,
    camera_angle, movement, lens, framing,
    duration, description, equipment_needed,
    notes, created_at
)
```

---

## 🔐 AUTENTICAÇÃO E PERMISSÕES

### Níveis de Usuário

```
1. Admin (você)
   - Acesso total
   - Gerenciar usuários
   - Ver todos projetos

2. Producer
   - Criar/editar projetos
   - Gerenciar equipe
   - Aprovar orçamentos
   - Solicitar análises IA

3. Crew Member
   - Ver projetos atribuídos
   - Visualizar call sheets
   - Reportar horas

4. Read-only
   - Visualizar apenas
   - Exportar relatórios
```

---

## 🌊 FLUXO DE TRABALHO TÍPICO

### Cenário 1: Novo Projeto

```
1. Producer cria projeto "Eclipse - O Filme"
2. Faz upload do roteiro (PDF)
3. Sistema extrai texto automaticamente
4. Producer clica "Analisar com Scripturemon"
5. IA analisa com 24 especialistas (rodando no VPS)
6. Resultados aparecem em "Análises" do projeto
7. Producer lê recomendações
8. Usa "Assistente de Breakdown" para extrair:
   - Equipamentos necessários → adiciona em "Equipamentos"
   - Locações → adiciona em "Locações"
   - Estimativa de equipe → monta em "Equipe"
9. IA sugere orçamento inicial
10. Producer ajusta e aprova
11. IA gera cronograma otimizado
12. Produção começa!
```

### Cenário 2: Pré-Produção Criativa

```
1. Diretor cria Mood Board "Look Visual - Eclipse"
2. Adiciona referências (Blade Runner, Her, etc.)
3. IA analisa e sugere paleta de cores: Azul cibernético + Laranja neon
4. Diretor cria Storyboard da cena 1
5. IA sugere 6 quadros baseado no roteiro
6. Diretor ajusta e aprova
7. Sistema gera Shotlist automaticamente
   - 12 planos identificados
   - Equipamentos sugeridos
8. Tasks criadas automaticamente:
   - "Alugar Steadicam para cena 1"
   - "Contratar maquiador cyberpunk"
9. Calendar atualizado com deadlines
```

### Cenário 3: Dia de Filmagem

```
1. Crew abre sistema no celular
2. Vê call sheet do dia (gerado da shotlist)
3. Confirma presença
4. Vê equipamentos alocados
5. Acessa mapa da locação
6. Marca shots como concluídos em tempo real
7. Reporta problemas
8. Sistema atualiza progresso automaticamente
```

---

## 🔗 INTEGRAÇÃO ENTRE MÓDULOS

**Fluxo Completo de Produção:**

```
ROTEIRO
   ↓
SCRIPTUREMON (análise de 24 especialistas)
   ↓
BREAKDOWN (IA extrai equipamentos, locações, personagens)
   ↓
┌─────────────────────────────────────────┐
│  MOOD BOARD → referências visuais      │
│  STORYBOARD → planejamento visual      │
│  SHOTLIST → lista de planos            │
│  TASKS → tarefas de produção           │
│  CALENDAR → cronograma                 │
└─────────────────────────────────────────┘
   ↓
ORÇAMENTO (IA calcula custos)
   ↓
EQUIPE (contratações)
   ↓
EQUIPAMENTOS (reservas)
   ↓
LOCAÇÕES (agendamentos)
   ↓
CALL SHEET (gerado da shotlist)
   ↓
FILMAGEM ✅
```

**Exemplo de Integração:**

1. **Roteiro → Storyboard:**
   - IA lê "INT. QUARTO - NOITE" e sugere composição

2. **Storyboard → Shotlist:**
   - Cada quadro vira 1-3 shots na shotlist

3. **Shotlist → Equipamentos:**
   - "Shot 5 precisa Dolly" → adiciona automaticamente

4. **Shotlist → Calendar:**
   - Estima 8h de filmagem → bloqueia no calendário

5. **Calendar → Tasks:**
   - "Filmagem em 3 dias" → cria task "Preparar equipamento"

6. **Tasks → Call Sheet:**
   - Tasks concluídas = call sheet pronto para enviar

7. **Mood Board → Storyboard:**
   - Referências visuais alimentam composições

---

## 🚀 FASES DE IMPLEMENTAÇÃO

### FASE 1: Setup Base (1-2 semanas)
- [ ] Criar estrutura Flask
- [ ] Setup PostgreSQL
- [ ] Migrar modelos de dados
- [ ] Sistema de autenticação
- [ ] Dashboard básico

### FASE 2: CRUD Básico (1-2 semanas)
- [ ] Projetos
- [ ] Equipe
- [ ] Equipamentos
- [ ] Locações
- [ ] Orçamento
- [ ] Documentos

### FASE 2.5: Módulos Criativos (2 semanas)
- [ ] **Mood Board**
  - Upload de imagens
  - Drag & drop de elementos
  - Visualização em grid
- [ ] **Tasks**
  - CRUD de tasks
  - Atribuição de responsáveis
  - Kanban board view
- [ ] **Calendar**
  - Visualização mensal/semanal
  - Integração com schedule_events
  - Detecção de conflitos
- [ ] **Storyboard**
  - Upload de frames
  - Informações técnicas por quadro
  - Exportar PDF
- [ ] **Shotlist**
  - Lista de planos detalhada
  - Campos técnicos (lente, ângulo, movimento)
  - Exportar para call sheet
- [ ] **Call Sheets**
  - Geração automática
  - Integração com shotlist
  - Email/SMS para equipe

### FASE 3: Integração Scripturemon (1 semana)
- [ ] Upload de roteiro
- [ ] Extração de texto (PDF → TXT)
- [ ] Integrar análise dos 24 especialistas
- [ ] Exibir resultados na interface
- [ ] Download de relatórios

### FASE 4: IA Multi-funcional (2-3 semanas)
- [ ] Setup Ollama no VPS
- [ ] LLM Service base
- [ ] Assistente de Breakdown
- [ ] Assistente de Orçamento
- [ ] Assistente de Cronograma
- [ ] Chat inteligente

### FASE 5: Deploy VPS (1 semana)
- [ ] Setup servidor
- [ ] Nginx + Gunicorn
- [ ] SSL/HTTPS
- [ ] Backup automático
- [ ] Monitoramento

### FASE 6: Refinamentos
- [ ] Mobile responsive
- [ ] Notificações
- [ ] Exportação de relatórios
- [ ] Integrações (Google Calendar, Slack, etc.)

---

## 💾 VPS - REQUISITOS TÉCNICOS

### Especificações Mínimas

```
CPU: 4 cores
RAM: 16GB (Ollama precisa de memória!)
Storage: 100GB SSD
OS: Ubuntu 22.04 LTS
```

### Software a Instalar

```bash
# Sistema
- Python 3.13
- PostgreSQL 15
- Redis
- Nginx
- Supervisor

# LLM
- Ollama
- Modelo: scripturemon-optimized (ou llama3/mistral)

# Segurança
- UFW (firewall)
- Fail2ban
- SSL/Let's Encrypt
```

---

## 📈 ESTIMATIVA DE CUSTOS MENSAIS

```
VPS (16GB RAM): $40-80/mês
Domain: $1/mês
SSL: Grátis (Let's Encrypt)
Backups: $10/mês
CDN (opcional): $5/mês

Total: ~$50-100/mês
```

---

## 🔄 PRÓXIMOS PASSOS

1. **Validar arquitetura** - Você aprova essa estrutura?
2. **Definir prioridades** - Quais módulos são mais urgentes?
3. **Escolher VPS** - DigitalOcean? AWS? Hetzner?
4. **Começar FASE 1** - Setup base do Flask

---

## 🤔 DECISÕES PENDENTES

1. **Frontend Framework:**
   - Manter JavaScript vanilla (mais simples)?
   - Usar Vue.js (mais reativo)?
   - React (mais complexo)?

2. **Modelos LLM:**
   - Ollama local (grátis, mais lento)?
   - OpenAI API (pago, mais rápido)?
   - Híbrido (Ollama + OpenAI para tarefas específicas)?

3. **Upload de arquivos:**
   - Armazenar no VPS?
   - Usar S3/CDN?

4. **Backup:**
   - Diário automático?
   - Onde armazenar (Backblaze B2, AWS S3)?

---

**Me diga:**
1. Essa arquitetura faz sentido pra você?
2. Tem algo que quer mudar/adicionar?
3. Qual VPS você tem? (specs)
4. Quer começar pela FASE 1 agora ou discutir mais?
