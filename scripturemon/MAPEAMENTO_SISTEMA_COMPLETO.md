# 🗺️ MAPEAMENTO COMPLETO DO SISTEMA - SCRIPTUREMON

**Data:** 2025-10-14
**Branch:** feature/gpt5-hybrid-backend
**Status:** Sistema configurado com OLD (scripturemon-optimized)

---

## 📁 ESTRUTURA DE DIRETÓRIOS

```
scripturemon/
├── engine/                      # Motor de análise
│   ├── analyzers/              # 26 analisadores (dr_*.py)
│   ├── exporters/              # Exportação formatada
│   ├── indexer/                # Indexação de teorias
│   ├── orchestration/          # Coordenação de análises
│   ├── prompts/                # Prompts por autor
│   └── utils/                  # Utilit\u00e1rios (checkpoint_manager)
│
├── inputs/                      # Roteiros de entrada
│   └── examples/               # Exemplos (Te Encontro em Mim.pdf)
│
├── knowledge/                   # Base de conhecimento teórica
│   ├── authors/                # Teorias por autor (12 autores)
│   └── mappings/               # Mapeamentos especialista-autor
│
├── workspace/                   # Área de trabalho (outputs)
│   ├── outputs/                # Análises completas
│   ├── checkpoints/            # Checkpoints de progresso
│   └── temp/                   # Arquivos temporários
│
├── config/                      # Configurações
│   ├── model_config.py         # Configuração de modelos LLM
│   └── rules/                  # Regras YAML (18 especialidades)
│
├── specialist_factory/          # Fábrica de especialistas
│
├── ui_design/                   # Interface web
│
├── tests/                       # Testes
│
├── archive/                     # Arquivos antigos
│
├── backups/                     # Backups
│
├── docs/                        # Documentação
│
└── logs/                        # Logs de execução

```

---

## 🧩 COMPONENTES PRINCIPAIS

### 1. **SCRIPTS PRINCIPAIS**

| Script | Função | Status |
|--------|--------|--------|
| `analyze_all_specialists.py` | Análise completa com todos os especialistas | ✅ Funcional |
| `analyze.py` | Análise individual | ✅ Funcional |
| `dashboard.py` | Dashboard web de monitoramento | ✅ Funcional |
| `web_server.py` | Servidor web para UI | ✅ Funcional |
| `setup_wizard.py` | Wizard de configuração inicial | ✅ Funcional |

### 2. **ENGINE DE ANÁLISE**

#### 2.1. Analisadores (`engine/analyzers/`)

26 analisadores especializados:

- **Estrutura:** `dr_structure.py`, `dr_pacing.py`, `dr_opening.py`, `dr_climax.py`, `dr_resolution.py`
- **Personagens:** `dr_character.py`, `dr_backstory.py`, `dr_motivation.py`
- **Diálogo:** `dr_dialogue.py`, `dr_subtext.py`, `dr_exposition.py`
- **Narrativa:** `dr_conflict.py`, `dr_tension.py`, `dr_stakes.py`, `dr_theme.py`
- **Elementos:** `dr_action.py`, `dr_symbolism.py`, `dr_worldbuilding.py`, `dr_foreshadowing.py`
- **Técnica:** `dr_tone.py`, `dr_genre.py`, `dr_transitions.py`, `dr_twist.py`
- **Avaliação:** `dr_evaluator.py`

Cada analisador:
- Define queries específicas para LLM
- Processa resposta do modelo
- Gera métricas quantitativas
- Produz análise qualitativa

#### 2.2. Orquestração (`engine/orchestration/`)

- **`dual_core_wrapper.py`** - Coordena análises duais (character/structure)

#### 2.3. Exportação (`engine/exporters/`)

- **`formatted_exporter.py`** - Gera outputs HTML formatados

#### 2.4. Utilit\u00e1rios (`engine/utils/`)

- **`checkpoint_manager.py`** - Gerencia checkpoints de progresso

---

### 3. **KNOWLEDGE BASE**

#### 3.1. Autores (`knowledge/authors/`)

12 teóricos de roteiro:

1. **Robert McKee** - Story (estrutura, personagem)
2. **Christopher Vogler** - The Writer's Journey (hero's journey)
3. **Syd Field** - Screenplay (paradigma de 3 atos)
4. **John Truby** - The Anatomy of Story (22 passos)
5. **Blake Snyder** - Save the Cat! (beat sheet)
6. **Linda Seger** - Making a Good Script Great
7. **Lajos Egri** - The Art of Dramatic Writing (premissa)
8. **K.M. Weiland** - Creating Character Arcs
9. **Aristotle** - Poetics (teoria clássica)
10. **Joseph Campbell** - The Hero with a Thousand Faces
11. **Linda Cowgill** - Writing Short Films
12. **David Howard & Edward Mabley** - The Tools of Screenwriting

Cada autor tem:
- Arquivo de indexação (estrutura + conceitos)
- Mapeamento para especialistas relevantes

#### 3.2. Mapeamentos (`knowledge/mappings/`)

Conecta especialidades aos autores apropriados.

Exemplo:
- `character` → McKee (Character), Truby, Weiland, Egri
- `structure` → Field, McKee (Structure), Snyder, Vogler
- `dialogue` → McKee (Dialogue), Truby

---

### 4. **MODELFILES OLLAMA**

Modelos configurados:

| Modelo | Status | Uso | Qualidade |
|--------|--------|-----|-----------|
| `scripturemon-optimized` (OLD) | ✅ **ATIVO** | Produção | 9/10 |
| `scripturemon-corrected` (NEW) | ⚠️ Deprecated | Teste | 2/10 |
| `scripturemon-balanced` | ⚠️ Incompleto | Teste | 6/10 |
| `scripturemon-old-plus` | ❌ Falhou | Teste | 3/10 |

**Configuração ativa:** `scripturemon-optimized` (OLD)
- Base: Mixtral 8x7B Instruct v0.1 Q5_K_M
- Temperature: 0.3 (analítico)
- Context: 32K real
- Output: 53K chars médio
- Tempo: ~103s por análise

---

### 5. **SISTEMA DE CHECKPOINT**

Gerencia progresso de análises longas:

**Estrutura:**
```
workspace/checkpoints/
└── [screenplay_hash]/
    └── checkpoint.json
```

**Dados salvos:**
- Especialistas completados
- Autores processados por especialista
- Timestamps
- Estado de continuação

**Comandos:**
```bash
python list_checkpoints.py          # Listar checkpoints
python cleanup_checkpoints.py       # Limpar checkpoints antigos
```

---

### 6. **DASHBOARD & MONITORAMENTO**

#### Dashboard Web (`dashboard.py`)

**URL:** http://localhost:5000

**Funcionalidades:**
- Visualização de análises em progresso
- Histórico de análises completas
- Métricas em tempo real
- Preview de resultados

**Iniciar:**
```bash
bash start_dashboard.sh
# ou
python3 dashboard.py
```

#### Scripts de Monitoramento

- `watch_progress.sh` - Monitora progresso em tempo real
- `watch_live.sh` - Watch live da análise
- `monitor_analysis.sh` - Monitor com logs

---

### 7. **OUTPUTS**

Análises geram:

```
workspace/outputs/[TITULO]_[timestamp]/
├── 1_raw_analyses/                  # Análises brutas por especialista
│   ├── character/
│   │   ├── mckee.txt
│   │   ├── truby.txt
│   │   └── ...
│   └── structure/
│       ├── field.txt
│       └── ...
│
├── 2_logs/
│   ├── analysis.log                 # Log principal
│   └── checkpoint.json              # Checkpoint
│
├── 3_consolidated/
│   └── full_analysis.json           # Análise consolidada
│
└── 4_formatted/
    └── [TITULO]_formatted.html      # HTML formatado
```

---

## 🔧 CONFIGURAÇÃO ATUAL

### Modelo LLM Ativo

```python
# analyze_all_specialists.py linha 566
llm_model = "scripturemon-optimized"  # OLD - confirmado melhor qualidade
```

### Parâmetros do OLD

```dockerfile
FROM mixtral:8x7b-instruct-v0.1-q5_K_M
PARAMETER temperature 0.3
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER min_p 0.05
PARAMETER num_ctx 131072    # Configurado mas real é 32K
PARAMETER num_predict -1    # Ilimitado
PARAMETER num_batch 64
```

### System Prompt

~8K caracteres focando em:
- Qualidade > Velocidade
- 4 problemas + 4 soluções obrigatórias
- 10-15K chars mínimo
- Estrutura 14 parágrafos
- Citações específicas do roteiro
- Fundamentação teórica com capítulos

---

## 🚀 COMANDOS PRINCIPAIS

### Análise Completa

```bash
# Análise automática (sem confirmação)
python3 analyze_all_specialists.py "inputs/examples/roteiro.pdf" --yes

# Com modelo específico
python3 analyze_all_specialists.py "roteiro.pdf" --model scripturemon-optimized

# Continuar checkpoint
python3 analyze_all_specialists.py "roteiro.pdf" --resume

# Com auto-avaliação GPT-5 (se disponível)
python3 analyze_all_specialists.py "roteiro.pdf" --yes --self-eval
```

### Análise Individual

```bash
# Um especialista, um autor
python3 analyze.py "roteiro.pdf" character mckee

# Com modelo específico
python3 analyze.py "roteiro.pdf" structure field --model scripturemon-optimized
```

### Dashboard

```bash
# Iniciar
bash start_dashboard.sh

# Parar
bash stop_dashboard.sh

# Manual
python3 dashboard.py
```

### Monitoramento

```bash
# Watch progress
bash watch_progress.sh

# Monitor live
bash watch_live.sh

# Custom monitor
bash monitor_analysis.sh
```

### Checkpoints

```bash
# Listar
python3 list_checkpoints.py

# Limpar antigos
python3 cleanup_checkpoints.py

# Limpar workspace
python3 cleanup_workspace.py
```

### Utilit\u00e1rios

```bash
# Comparar análises
python3 compare_analyses.py output1/ output2/

# Consolidar análises
python3 consolidate_analyses.py output_folder/

# Histórico
python3 analysis_history.py

# Estatísticas de uso
python3 usage_stats.py

# Preview de análise
python3 analysis_preview.py output_folder/
```

---

## 📊 ESPECIALISTAS × AUTORES

### Mapeamento Completo

| Especialista | Autores Suportados | Principal |
|--------------|-------------------|-----------|
| **character** | McKee, Truby, Weiland, Egri | McKee |
| **structure** | Field, McKee, Snyder, Vogler | Field |
| **dialogue** | McKee, Truby | McKee |
| **conflict** | McKee, Truby, Egri | McKee |
| **theme** | McKee, Truby, Egri | McKee |
| **pacing** | Field, McKee | Field |
| **backstory** | Truby, Weiland | Truby |
| **motivation** | Truby, Egri, Weiland | Egri |
| **opening** | Field, Snyder, McKee | Field |
| **climax** | McKee, Field, Vogler | McKee |
| **resolution** | McKee, Field | McKee |
| **worldbuilding** | Vogler, Truby | Truby |
| **symbolism** | Vogler, Campbell | Vogler |
| **tension** | McKee, Field | McKee |
| **stakes** | Truby, McKee | Truby |
| **subtext** | McKee, Truby | McKee |
| **exposition** | Field, McKee | McKee |
| **genre** | Snyder, McKee | Snyder |
| **action** | Field, Snyder | Field |
| **foreshadowing** | Field, Truby | Truby |
| **tone** | McKee, Field | McKee |
| **transitions** | Field, McKee | Field |
| **twist** | Field, Truby | Truby |

Total: 23 especialistas × média 2-3 autores cada = ~50 análises por roteiro

---

## 🔄 FLUXO DE EXECUÇÃO

### 1. Início da Análise

```
analyze_all_specialists.py
  ↓
Carrega configurações
  ↓
Verifica checkpoint existente
  ↓
Extrai texto do PDF
  ↓
Gera hash do roteiro
  ↓
Cria estrutura de outputs
```

### 2. Loop de Análise

```
Para cada especialista:
  ↓
  Para cada autor:
    ↓
    Carrega teoria do autor (knowledge/authors/)
    ↓
    Carrega queries do analisador (engine/analyzers/)
    ↓
    Gera prompt completo
    ↓
    Chama Ollama (scripturemon-optimized)
    ↓
    Processa resposta
    ↓
    Salva raw analysis
    ↓
    Atualiza checkpoint
    ↓
    Log progresso
```

### 3. Consolidação

```
Todas as análises completas
  ↓
Consolida JSON
  ↓
Gera HTML formatado
  ↓
Calcula métricas finais
  ↓
Salva output final
```

---

## 🐛 DEBUGGING & LOGS

### Arquivos de Log

```bash
workspace/outputs/[analise]/2_logs/analysis.log  # Log principal
full_analysis_log.txt                            # Log global
analysis_progress.log                            # Progresso
test_full.log                                    # Testes
```

### Verificar Status

```bash
# Ver progresso
tail -f full_analysis_log.txt

# Ver checkpoint
cat workspace/outputs/[analise]/2_logs/checkpoint.json | jq

# Contar análises completas
find workspace/outputs -name "*.txt" | wc -l

# Ver especialistas pendentes
python3 list_checkpoints.py
```

---

## 🔐 SISTEMA DE MEMÓRIA

**Nota:** Sistema MEMORY/ não está presente nesta instância do scripturemon.

Se necessário implementar:
```bash
mkdir MEMORY
# Adicionar scripts de memória persistente
# (Ver outros projetos do usuário para referência)
```

---

## ⚙️ VARIÁVEIS DE AMBIENTE

```bash
# .env (se existir)
OLLAMA_HOST=http://localhost:11434
GPT5_API_KEY=[se configurado]
```

Carregar:
```bash
source load_env.sh
```

---

## 📦 DEPENDÊNCIAS

### Python Requirements

```
pypdf2
pydantic
flask
jinja2
```

### Modelos Ollama

```bash
# Listar modelos instalados
ollama list | grep scripturemon

# Modelo ativo
scripturemon-optimized (76e8c7391316, 33 GB)
```

---

## 🧪 TESTES

```bash
# Testes gerais
pytest tests/

# Teste integração app
bash test_app_integration.sh

# Teste específico
python3 test_anti_hallucination.py
python3 test_ner_validation.py
```

---

## 📚 DOCUMENTAÇÃO RECENTE

Documentos criados nesta sessão:

1. `COMPARACAO_FINAL_4_MODELOS.md` - Teste comparativo OLD vs NEW vs BALANCED vs OLD+
2. `ANALISE_QUALITATIVA_SCRIPT_DOCTOR.md` - Análise profissional dos modelos
3. `RESULTADO_FINAL.md` - Conclusão: OLD é o melhor
4. `EXPLICACAO_OLD_PLUS.md` - Tentativa de otimização (falhou)
5. `RESUMO_OLD_PLUS.md` - Resumo rápido do OLD+
6. `EXPLICACAO_OPCAO_C_BALANCED.md` - Sobre o modelo BALANCED
7. `RESUMO_OPCAO_C.md` - Resumo do BALANCED

---

## ✅ STATUS ATUAL DO SISTEMA

### ✅ Funcionando

- ✅ Análise completa (`analyze_all_specialists.py`)
- ✅ Análise individual (`analyze.py`)
- ✅ Sistema de checkpoint
- ✅ Dashboard web
- ✅ Modelo OLD (scripturemon-optimized) - 9/10 qualidade
- ✅ 26 analisadores especializados
- ✅ 12 teorias de roteiro indexadas
- ✅ Exportação HTML formatada
- ✅ Monitoramento em tempo real

### ⚠️ Necessita Atenção

- ⚠️ Git com muitos arquivos não rastreados (fora do repo)
- ⚠️ Background processes órfãos (já finalizados)
- ⚠️ Sistema MEMORY/ não implementado nesta instância

### ❌ Não Funcional

- ❌ Modelo BALANCED (trunca em 2/4 problemas)
- ❌ Modelo OLD+ (falhou completamente)
- ❌ Modelo NEW (genérico demais)

---

## 🎯 PRÓXIMOS PASSOS RECOMENDADOS

1. **Git Cleanup** - Commit/limpar arquivos não rastreados
2. **Sistema de Memória** - Implementar se necessário
3. **Fix BALANCED** - Investigar truncamento (potencial melhoria)
4. **Documentação** - Atualizar README principal

---

## 🔗 REFERÊNCIAS

- Branch: `feature/gpt5-hybrid-backend`
- Último commit: `c679e58 Docs: Add NER HTML report test documentation`
- Modelo ativo: `scripturemon-optimized`
- Working directory: `/Users/clubproducoes/Digimundo/scripturemon`

---

**🎬 Sistema mapeado e funcional!**

Para usar:
```bash
python3 analyze_all_specialists.py "inputs/examples/Te Encontro em Mim .pdf" --yes
```
