# 📋 CATEGORIZAÇÃO DE ARQUIVOS DO SISTEMA

**Data:** 2025-10-14
**Objetivo:** Identificar arquivos essenciais vs obsoletos para limpeza

---

## ✅ ARQUIVOS ESSENCIAIS (Manter na Raiz)

### Scripts Principais

```
analyze_all_specialists.py  ⭐ PRINCIPAL - Análise completa 24×13
analyze.py                  📝 Análise individual de 1 especialista
consolidate_analyses.py     🔄 Consolidação de HTMLs
dashboard.py                📊 Dashboard web de monitoramento
web_server.py               🌐 Servidor web para UI
setup_wizard.py             🧙 Wizard de configuração inicial
```

### Utilitários Essenciais

```
cleanup_checkpoints.py      🧹 Limpar checkpoints antigos
cleanup_workspace.py        🗑️  Limpar workspace
list_checkpoints.py         📋 Listar checkpoints existentes
usage_stats.py              📊 Estatísticas de uso
analysis_history.py         📖 Histórico de análises
analysis_preview.py         👁️  Preview de análises
```

### Scripts Shell

```
load_env.sh                 🔑 Carregar variáveis de ambiente
start_dashboard.sh          ▶️  Iniciar dashboard
stop_dashboard.sh           ⏹️  Parar dashboard
monitor_analysis.sh         📡 Monitorar análise
watch_progress.sh           👀 Watch progresso
watch_live.sh               📺 Watch live
```

### Modelfiles

```
Modelfile.anti-hallucination   🧪 Anti-alucinação
Modelfile.balanced            ⚖️  Balanced (incompleto)
Modelfile.corrected           ✏️  NEW/Corrected (deprecated)
Modelfile.old_plus            ➕ OLD+ (falhou)

Nota: scripturemon-optimized (OLD) já está no Ollama
```

---

## 📚 DOCUMENTAÇÃO ESSENCIAL (Manter na Raiz)

### Documentação Principal

```
README.md                              📖 README principal
README_SISTEMA_ATUAL.md                📋 Documentação do sistema atual
MAPEAMENTO_SISTEMA_COMPLETO.md         🗺️  Mapa completo (NOVO - 2025-10-14)
```

### Documentação de Decisões (Manter)

```
RESULTADO_FINAL.md                     ✅ Decisão final sobre modelos
COMPARACAO_FINAL_4_MODELOS.md          📊 Comparação técnica detalhada
ANALISE_QUALITATIVA_SCRIPT_DOCTOR.md   🎬 Análise profissional
RESUMO_SESSAO_2025-10-14.md            📝 Resumo da sessão atual
```

---

## 🗑️ ARQUIVOS PARA ARQUIVAR

### Testes (Mover para archive/tests/)

```
test_anti_hallucination.py             🧪 Teste anti-alucinação
test_gpt5_quick.py                     🧪 Teste rápido GPT-5
test_ner_html_report.py                🧪 Teste NER HTML
test_ner_validation.py                 🧪 Teste validação NER
test_new_naming.py                     🧪 Teste naming
test_simple_validation.py              🧪 Teste validação simples
test_app_integration.sh                🧪 Teste integração app
```

### Scripts Utilitários Pontuais (Mover para archive/utils/)

```
benchmark_performance.py                📊 Benchmark de performance
checkpoint_manager_improved.py          🔧 Checkpoint manager melhorado (não usado)
fix_unknown_folders.py                  🔧 Fix pontual de pastas
migrate_old_folders.py                  🔧 Migração pontual
reorganize_specialist_folders.py        🔧 Reorganização pontual
model_comparison.py                     🔧 Comparação de modelos
partial_analysis.py                     🔧 Análise parcial (não usado)
compare_analyses.py                     🔧 Comparação de análises
web_server_backup_simple.py             🔧 Backup do servidor web
```

### Documentação de Sessões Antigas (Mover para archive/docs/sessions/)

```
ANALISE_APP_E_DASHBOARD.md              📄 Análise app (sessão antiga)
ANALISE_ESTRUTURA_PASTA_COMPLETA.md     📄 Análise estrutura (sessão antiga)
ANALISE_QUALIDADE_PRIMEIROS_RESULTADOS.md 📄 Primeiros resultados
APP_DEBUGGING_REPORT.md                 📄 Debug app
BUG_REPORT_MISSING_PDF_LOADER.md        📄 Bug PDF loader
COMPARACAO_DIRETA_MODELOS.md            📄 Comparação direta
COMPARACAO_PRIMEIRA_ANALISE.md          📄 Primeira comparação
COMPARACAO_VISUAL_MODELFILES.md         📄 Comparação visual
CRITICAL_HALLUCINATION_REPORT.md        📄 Report alucinação
DIAGNOSTIC_REPORT_TEE_VS_REDIRECT.md    📄 Diagnóstico tee
FIX_APPLIED_SUMMARY.md                  📄 Summary fix
IMPLEMENTACAO_COMPLETA.md               📄 Implementação completa
INTEGRATION_REPORT_v11.md               📄 Report integração
INVESTIGATION_COMPLETE_REPORT.md        📄 Report investigação
MASTER_DOCUMENTO_BUG_E_CORRECAO.md      📄 Documento bugs
MONITORING_GUIDE.md                     📄 Guia monitoramento
NER_IMPLEMENTATION_SUMMARY.md           📄 Summary NER
PROCESS_COMPLETE_ANALYSIS.md            📄 Process análise
PROMPT_NER_RESEARCH.md                  📄 Research NER
QUALITY_AUDIT_REPORT_2025-10-11.md      📄 Audit qualidade
QUERY_OPTIMIZATION_CHECKPOINT.md        📄 Otimização queries
RESEARCH_PROMPTS_BY_PLATFORM.md         📄 Research prompts
RESEARCH_PROMPT_MODELFILE_OPTIMIZATION.md 📄 Research Modelfile
RESULTADO_9_ANALISES.md                 📄 Resultado 9 análises
SESSION_UPDATE_2025-10-12.md            📄 Update sessão
SOLUCAO_DEFINITIVA_BASEADA_EM_PERPLEXITY.md 📄 Solução Perplexity
SPECIALIST_FACTORY_CRIADO.md            📄 Specialist factory
STATUS_IMPLEMENTACAO.md                 📄 Status implementação
SYSTEM_COMPLETE_AUDIT.md                📄 Audit sistema
TEE_ADVANTAGES_AND_HISTORY.md           📄 Tee advantages
TEST_NER_HTML_REPORT.md                 📄 Test NER report
TEST_REPORT.md                          📄 Test report
UI_DESIGN_REPORT.md                     📄 UI design
UI_INTEGRATION_REPORT.md                📄 UI integration
```

### Documentação Experimentos Modelos (Mover para archive/docs/model_experiments/)

```
EXPLICACAO_OLD_PLUS.md                  📄 Explicação OLD+
RESUMO_OLD_PLUS.md                      📄 Resumo OLD+
EXPLICACAO_OPCAO_C_BALANCED.md          📄 Explicação BALANCED
RESUMO_OPCAO_C.md                       📄 Resumo BALANCED
```

### Arquivos Temporários (Deletar)

```
.clean                                  🗑️  Arquivo temp
analysis_pid.txt                        🗑️  PID temporário
full_analysis_log.txt                   🗑️  Log temporário
```

### PDFs (Mover para docs/)

```
"Solving Ollama Modelfile Truncation with Mixtral 8x7B_ Context Limits and Sampling Parameters.pdf"
```

---

## 📁 ESTRUTURA FINAL DESEJADA

```
scripturemon/
├── analyze_all_specialists.py  ⭐ PRINCIPAL
├── analyze.py
├── consolidate_analyses.py
├── dashboard.py
├── web_server.py
├── setup_wizard.py
├── cleanup_checkpoints.py
├── cleanup_workspace.py
├── list_checkpoints.py
├── usage_stats.py
├── analysis_history.py
├── analysis_preview.py
│
├── *.sh                        (6 scripts shell)
├── Modelfile.*                 (4 modelfiles)
│
├── README.md
├── README_SISTEMA_ATUAL.md
├── MAPEAMENTO_SISTEMA_COMPLETO.md
├── RESULTADO_FINAL.md
├── COMPARACAO_FINAL_4_MODELOS.md
├── ANALISE_QUALITATIVA_SCRIPT_DOCTOR.md
├── RESUMO_SESSAO_2025-10-14.md
├── ARQUIVOS_SISTEMA_CATEGORIZADO.md
│
├── engine/                     ✅ NÃO MEXER
├── knowledge/                  ✅ NÃO MEXER (conforme solicitado)
├── inputs/                     ✅ NÃO MEXER (conforme solicitado)
├── workspace/                  ✅ NÃO MEXER
├── config/                     ✅ NÃO MEXER
├── specialist_factory/         ✅ NÃO MEXER
├── ui_design/                  ✅ NÃO MEXER
├── tests/                      ✅ NÃO MEXER
├── logs/                       ✅ NÃO MEXER
├── outputs/                    ✅ NÃO MEXER
├── backups/                    ✅ NÃO MEXER
├── docs/                       ✅ NÃO MEXER
│
└── archive/                    📦 DESTINO DOS OBSOLETOS
    ├── tests/                  → test_*.py
    ├── utils/                  → scripts pontuais
    ├── docs/
    │   ├── sessions/           → docs de sessões antigas
    │   └── model_experiments/  → docs de experimentos
    └── old_modelfiles/         (já existe)
```

---

## 🎯 PLANO DE LIMPEZA

### 1. Criar Estrutura de Archive

```bash
mkdir -p archive/tests
mkdir -p archive/utils
mkdir -p archive/docs/sessions
mkdir -p archive/docs/model_experiments
mkdir -p archive/docs/pdfs
```

### 2. Mover Testes

```bash
mv test_*.py archive/tests/
mv test_app_integration.sh archive/tests/
```

### 3. Mover Utilitários Pontuais

```bash
mv benchmark_performance.py archive/utils/
mv checkpoint_manager_improved.py archive/utils/
mv fix_unknown_folders.py archive/utils/
mv migrate_old_folders.py archive/utils/
mv reorganize_specialist_folders.py archive/utils/
mv model_comparison.py archive/utils/
mv partial_analysis.py archive/utils/
mv compare_analyses.py archive/utils/
mv web_server_backup_simple.py archive/utils/
```

### 4. Mover Documentação Antiga

```bash
mv ANALISE_*.md archive/docs/sessions/ 2>/dev/null
mv APP_*.md archive/docs/sessions/ 2>/dev/null
mv BUG_*.md archive/docs/sessions/ 2>/dev/null
mv COMPARACAO_PRIMEIRA*.md archive/docs/sessions/ 2>/dev/null
mv COMPARACAO_VISUAL*.md archive/docs/sessions/ 2>/dev/null
mv CRITICAL_*.md archive/docs/sessions/ 2>/dev/null
mv DIAGNOSTIC_*.md archive/docs/sessions/ 2>/dev/null
mv FIX_*.md archive/docs/sessions/ 2>/dev/null
mv IMPLEMENTACAO_*.md archive/docs/sessions/ 2>/dev/null
mv INTEGRATION_*.md archive/docs/sessions/ 2>/dev/null
mv INVESTIGATION_*.md archive/docs/sessions/ 2>/dev/null
mv MASTER_*.md archive/docs/sessions/ 2>/dev/null
mv MONITORING_*.md archive/docs/sessions/ 2>/dev/null
mv NER_*.md archive/docs/sessions/ 2>/dev/null
mv PROCESS_*.md archive/docs/sessions/ 2>/dev/null
mv PROMPT_*.md archive/docs/sessions/ 2>/dev/null
mv QUALITY_*.md archive/docs/sessions/ 2>/dev/null
mv QUERY_*.md archive/docs/sessions/ 2>/dev/null
mv RESEARCH_*.md archive/docs/sessions/ 2>/dev/null
mv RESULTADO_9*.md archive/docs/sessions/ 2>/dev/null
mv SESSION_*.md archive/docs/sessions/ 2>/dev/null
mv SOLUCAO_*.md archive/docs/sessions/ 2>/dev/null
mv SPECIALIST_*.md archive/docs/sessions/ 2>/dev/null
mv STATUS_*.md archive/docs/sessions/ 2>/dev/null
mv SYSTEM_*.md archive/docs/sessions/ 2>/dev/null
mv TEE_*.md archive/docs/sessions/ 2>/dev/null
mv TEST_*.md archive/docs/sessions/ 2>/dev/null
mv UI_*.md archive/docs/sessions/ 2>/dev/null
```

### 5. Mover Docs de Experimentos

```bash
mv EXPLICACAO_OLD_PLUS.md archive/docs/model_experiments/
mv RESUMO_OLD_PLUS.md archive/docs/model_experiments/
mv EXPLICACAO_OPCAO_C_BALANCED.md archive/docs/model_experiments/
mv RESUMO_OPCAO_C.md archive/docs/model_experiments/
mv COMPARACAO_DIRETA_MODELOS.md archive/docs/model_experiments/
```

### 6. Mover PDFs

```bash
mv *.pdf archive/docs/pdfs/ 2>/dev/null
```

### 7. Deletar Temporários

```bash
rm -f .clean analysis_pid.txt full_analysis_log.txt
```

---

## ✅ RESULTADO ESPERADO

**Raiz limpa com apenas:**
- 12 scripts .py essenciais
- 6 scripts .sh
- 4 Modelfiles
- 8 arquivos .md de documentação principal
- Diretórios intactos (engine/, knowledge/, inputs/, etc.)

**Total:** ~30 arquivos na raiz (vs ~80+ atuais)

---

**Criado:** 2025-10-14
**Para:** Limpeza e organização do sistema
