# 🎬 SCRIPTUREMON - Sistema Atual (2025-10-14)

## 📊 Scripts Principais

### 1. `analyze_all_specialists.py` ⭐ PRINCIPAL
**O QUE FAZ:**
- Analisa roteiro com TODOS os 24 especialistas
- Cada especialista analisa com 13 autores teóricos
- **Total: 24 × 13 = 312 análises individuais**
- Gera HTMLs individuais + consolidados
- Sistema com checkpoint (pode continuar de onde parou)

**COMO USAR:**
```bash
# Ollama (local, gratuito) - scripturemon-optimized (OLD)
python3 analyze_all_specialists.py "inputs/examples/roteiro.pdf" --yes
```

**MODELO ATUAL:**
- **scripturemon-optimized** (OLD) - Qualidade 9/10
- Base: Mixtral 8x7B Instruct v0.1 Q5_K_M
- Context: 32K
- Tempo: ~103s por análise
- Output: ~53K chars por análise

**TEMPO ESTIMADO:**
- Análise completa: ~8-10 horas

**SAÍDA:**
```
workspace/outputs/ROTEIRO__all_specialists_XXXX/
├── 1_individuais/
│   ├── CHARACTER/
│   │   ├── ANALISE_CHARACTER_MCKEE_20251014.html
│   │   ├── ANALISE_CHARACTER_FIELD_20251014.html
│   │   └── ... (13 HTMLs por especialista)
│   ├── STRUCTURE/
│   └── ... (24 especialistas)
├── 2_logs/
│   └── checkpoint.json
└── 3_consolidados/
    ├── CONSOLIDADO_CHARACTER_20251014.html
    └── ... (24 consolidados)
```

---

### 2. `analyze.py` 📝 ANÁLISE INDIVIDUAL
**O QUE FAZ:**
- Analisa roteiro com 1 especialista específico
- Útil para testes ou análises pontuais

---

### 3. `consolidate_analyses.py` 🔄 CONSOLIDAÇÃO
**O QUE FAZ:**
- Consolida múltiplos HTMLs em um único arquivo
- Usado automaticamente por `analyze_all_specialists.py`

---

### 4. `dashboard.py` 📊 DASHBOARD WEB
**O QUE FAZ:**
- Dashboard web para monitorar análises em tempo real
- Visualização de progresso

**COMO USAR:**
```bash
bash start_dashboard.sh
# Acesse http://localhost:5000
```

---

### 5. `web_server.py` 🌐 SERVIDOR WEB
**O QUE FAZ:**
- Servidor web para UI do sistema

---

### 6. `setup_wizard.py` 🧙 WIZARD DE CONFIGURAÇÃO
**O QUE FAZ:**
- Wizard interativo para configurar o sistema pela primeira vez

---

## 🔧 Scripts Utilitários

### `cleanup_checkpoints.py` 🧹
Limpar checkpoints antigos de análises anteriores

### `cleanup_workspace.py` 🗑️
Limpar workspace de outputs antigos

### `list_checkpoints.py` 📋
Listar todos os checkpoints existentes

### `usage_stats.py` 📊
Estatísticas de uso do sistema

### `analysis_history.py` 📖
Histórico de todas as análises realizadas

### `analysis_preview.py` 👁️
Preview de análises antes de rodar completo

---

## 📜 Scripts Shell

### `load_env.sh` 🔑
Carregar variáveis de ambiente (.env)

### `start_dashboard.sh` ▶️
Iniciar dashboard web

### `stop_dashboard.sh` ⏹️
Parar dashboard web

### `monitor_analysis.sh` 📡
Monitorar análise em execução

### `watch_progress.sh` 👀
Watch contínuo do progresso

### `watch_live.sh` 📺
Watch live de logs

---

## 📁 Estrutura de Pastas

```
scripturemon/
├── 📝 Scripts Python (10)
│   ├── analyze_all_specialists.py  ⭐ PRINCIPAL
│   ├── analyze.py                  📝 Individual
│   ├── consolidate_analyses.py     🔄 Consolidação
│   ├── dashboard.py                📊 Dashboard
│   ├── web_server.py               🌐 Servidor web
│   ├── setup_wizard.py             🧙 Wizard
│   ├── cleanup_checkpoints.py      🧹 Limpeza
│   ├── cleanup_workspace.py        🗑️  Workspace
│   ├── list_checkpoints.py         📋 Listar
│   ├── usage_stats.py              📊 Stats
│   ├── analysis_history.py         📖 Histórico
│   └── analysis_preview.py         👁️  Preview
│
├── 📜 Scripts Shell (5)
│   ├── load_env.sh                 🔑 Env vars
│   ├── start_dashboard.sh          ▶️  Start
│   ├── stop_dashboard.sh           ⏹️  Stop
│   ├── monitor_analysis.sh         📡 Monitor
│   ├── watch_progress.sh           👀 Watch
│   └── watch_live.sh               📺 Live
│
├── 📋 Modelfiles (4)
│   ├── Modelfile.anti-hallucination  🧪 Experimento
│   ├── Modelfile.balanced            ⚖️  Balanced (incompleto)
│   ├── Modelfile.corrected           ✏️  NEW (deprecated)
│   └── Modelfile.old_plus            ➕ OLD+ (falhou)
│
├── 📄 Documentação (8)
│   ├── README.md                              📖 README principal
│   ├── README_SISTEMA_ATUAL.md                📋 Este documento
│   ├── MAPEAMENTO_SISTEMA_COMPLETO.md         🗺️  Mapa completo
│   ├── RESULTADO_FINAL.md                     ✅ Decisão modelos
│   ├── COMPARACAO_FINAL_4_MODELOS.md          📊 Comparação técnica
│   ├── ANALISE_QUALITATIVA_SCRIPT_DOCTOR.md   🎬 Análise profissional
│   ├── RESUMO_SESSAO_2025-10-14.md            📝 Resumo sessão
│   └── ARQUIVOS_SISTEMA_CATEGORIZADO.md       🗂️  Categorização
│
├── 🏗️ Diretórios do Sistema
│   ├── engine/
│   │   ├── analyzers/              ← 26 especialistas (dr_*.py)
│   │   ├── core/                   ← Núcleo do sistema
│   │   └── orchestration/          ← Orquestração
│   │
│   ├── knowledge/                  ← 12 autores de teoria
│   │   ├── mckee/
│   │   ├── field/
│   │   ├── vogler/
│   │   └── ... (9 outros)
│   │
│   ├── workspace/
│   │   └── outputs/                ← Saídas das análises
│   │
│   ├── config/                     ← Configurações
│   ├── specialist_factory/         ← Factory de especialistas
│   ├── ui_design/                  ← Design UI
│   ├── tests/                      ← Testes
│   ├── logs/                       ← Logs
│   └── backups/                    ← Backups
│
└── archive/                        ← Arquivos obsoletos
    ├── tests/                      ← test_*.py (7 arquivos)
    ├── utils/                      ← Scripts pontuais (9 arquivos)
    └── docs/
        ├── sessions/               ← Docs antigas (33 arquivos)
        ├── model_experiments/      ← Experimentos (5 arquivos)
        └── pdfs/                   ← PDFs arquivados
```

---

## 📊 Modelo LLM Atual

### scripturemon-optimized (OLD) ✅

**Decisão baseada em testes comparativos:**
- Testados 4 modelos diferentes (OLD, NEW, BALANCED, OLD+)
- OLD venceu com **9/10 em qualidade**
- Único modelo com profundidade real e especificidade

**Configuração:**
```
Base: Mixtral 8x7B Instruct v0.1 Q5_K_M
Size: 33 GB
Temperature: 0.3
Context: 32K
Top-k: 40
Top-p: 0.9
Min-p: 0.05
Num_predict: -1 (ilimitado)
Num_batch: 64
```

**Performance:**
- Tempo: ~103s por análise
- Output: ~53K chars
- Qualidade: 9/10 (comprovada em 143 análises anteriores)

**Características:**
- ✅ Específico (cita páginas, cenas, diálogos exatos)
- ✅ Completo (sempre 4 problemas + 4 soluções)
- ✅ Profundo (53K chars = múltiplos exemplos e nuances)
- ✅ Confiável (não alucina, não trunca)
- ✅ Útil (Script Doctor pode trabalhar com a análise)

**Ver mais:**
- `RESULTADO_FINAL.md` - Decisão final
- `COMPARACAO_FINAL_4_MODELOS.md` - Análise técnica dos 4 modelos
- `ANALISE_QUALITATIVA_SCRIPT_DOCTOR.md` - Análise profissional

---

## 🚨 Arquivos Arquivados

Arquivos obsoletos foram movidos para `archive/` (2025-10-14):

**archive/tests/** (7 arquivos)
- test_anti_hallucination.py
- test_gpt5_quick.py
- test_ner_html_report.py
- test_ner_validation.py
- test_new_naming.py
- test_simple_validation.py
- test_app_integration.sh

**archive/utils/** (9 arquivos)
- benchmark_performance.py
- checkpoint_manager_improved.py
- fix_unknown_folders.py
- migrate_old_folders.py
- reorganize_specialist_folders.py
- model_comparison.py
- partial_analysis.py
- compare_analyses.py
- web_server_backup_simple.py

**archive/docs/sessions/** (33 arquivos)
- Documentação de sessões antigas (2025-10-10 até 2025-10-13)
- Reports de debugging, integração, NER, qualidade, etc.

**archive/docs/model_experiments/** (5 arquivos)
- EXPLICACAO_OLD_PLUS.md
- RESUMO_OLD_PLUS.md
- EXPLICACAO_OPCAO_C_BALANCED.md
- RESUMO_OPCAO_C.md
- COMPARACAO_DIRETA_MODELOS.md

---

## 🎯 Uso Rápido

**Rodar análise completa:**
```bash
python3 analyze_all_specialists.py "inputs/examples/roteiro.pdf" --yes
```

**Monitorar progresso:**
```bash
bash watch_progress.sh
# ou
bash monitor_analysis.sh
```

**Iniciar dashboard:**
```bash
bash start_dashboard.sh
# Acesse http://localhost:5000
```

**Verificar modelo ativo:**
```bash
ollama list | grep scripturemon-optimized
```

---

## 📚 Documentação Completa

Para entender o sistema completo, consulte:
- `MAPEAMENTO_SISTEMA_COMPLETO.md` - Mapa completo de todos os componentes
- `RESULTADO_FINAL.md` - Decisão sobre modelos
- `RESUMO_SESSAO_2025-10-14.md` - Resumo da última sessão

---

**Última atualização:** 2025-10-14
**Versão:** Sistema limpo e otimizado (24 Specialists × 13 Authors = 312 análises)
**Modelo:** scripturemon-optimized (OLD) - Qualidade 9/10
