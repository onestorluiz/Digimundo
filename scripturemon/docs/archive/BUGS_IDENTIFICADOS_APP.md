# 🐛 BUGS IDENTIFICADOS - ANALYZE SCREENPLAY APP

**Data**: 10 de Outubro de 2025
**App**: `/Applications/Analyze Screenplay.app`
**Status**: 🔴 DESALINHADO COM SISTEMA ATUAL

---

## 🎯 PROBLEMAS CRÍTICOS

### 1. ❌ SCRIPT ERRADO (CRÍTICO)

**Localização**: `/Applications/Analyze Screenplay.app/Contents/MacOS/run:301`

**Problema**:
```bash
# ❌ ERRADO - App atual (linha 301)
python3 analyze_with_checkpoints.py '$screenplay_file' $authors_flag --deep
```

**Deveria ser**:
```bash
# ✅ CORRETO - Sistema atual (FASE 3)
python3 analyze.py "$screenplay_file" --authors $authors_list --deep --use-personalized-prompts
```

**Impacto**:
- ❌ Não usa prompts personalizados (FASE 2)
- ❌ Não usa validação nivel 10 (FASE 3)
- ❌ Análises com qualidade inferior (Fase 1 vs Fase 3)
- ❌ Resultados 6-7/10 em vez de 15.5-18.0/10

---

### 2. ❌ PARÂMETROS INCORRETOS

**Problema**: App não usa os parâmetros corretos do `analyze.py`

**App atual**:
```bash
analyze_with_checkpoints.py <screenplay> [--all] --deep
```

**Sistema correto**:
```bash
analyze.py <screenplay>
  --authors <lista>         # aristotle, vogler, etc.
  --deep                     # deep context (128k tokens)
  --use-personalized-prompts # FASE 2 (crucial!)
```

---

### 3. ❌ FALTA VALIDAÇÃO DE PDF

**Problema**: App não valida qual PDF está sendo analisado

**Consequências**:
- Pode analisar PDF errado se houver múltiplos em `inputs/examples/`
- Sem confirmação visual do arquivo selecionado
- Usuário não tem certeza do que será analisado

**Solução Necessária**:
```bash
# Adicionar confirmação com preview
echo "📄 Analisando: $(basename "$screenplay_file")"
echo "📏 Tamanho: $(du -h "$screenplay_file" | cut -f1)"
echo "📅 Modificado: $(stat -f %Sm "$screenplay_file")"
```

---

### 4. ❌ MODO "DIALOGUE ONLY" INCORRETO

**Problema**: Modo "Dialogue Only" não especifica autor

**App atual (linha 290-294)**:
```bash
if [ "$analysis_mode" = "All 13" ]; then
    authors_flag="--all"
fi
# ❌ Se não for "All 13", authors_flag fica vazio!
```

**Deveria ser**:
```bash
if [ "$analysis_mode" = "All 13" ]; then
    authors_list="aristotle campbell cowgill dialogue egri field mckee mckee_character mckee_dialogue seger snyder truby vogler"
else
    authors_list="dialogue"  # ✅ Especificar autor
fi
```

---

### 5. ⚠️ FALTA FEEDBACK VISUAL

**Problema**: Usuário não sabe se análise está rodando

**Necessário**:
- Notificação inicial com tempo estimado
- Notificação intermediária aos 50%
- Notificação final com link para o HTML
- Indicador de progresso no Terminal

---

## 📊 COMPARAÇÃO DE RESULTADOS

### ❌ App Atual (analyze_with_checkpoints.py)

| Métrica | Resultado |
|---------|-----------|
| Script | analyze_with_checkpoints.py |
| Prompts | Genéricos |
| Validação | Sem nivel 10 |
| Score | 6-7/10 |
| Tamanho | 7-12KB |
| Tempo | ~40s |

### ✅ Sistema Correto (analyze.py --use-personalized-prompts)

| Métrica | Resultado |
|---------|-----------|
| Script | analyze.py |
| Prompts | Personalizados por autor |
| Validação | Nivel 10 ativo |
| Score | **15.5-18.0/10** |
| Tamanho | **15-22KB** |
| Tempo | 5-7min |

**Diferença**: +150% em qualidade! 🚀

---

## 🔧 CORREÇÕES NECESSÁRIAS

### Prioridade ALTA

1. **Atualizar script chamado**
   - Trocar `analyze_with_checkpoints.py` → `analyze.py`
   - Adicionar `--use-personalized-prompts`

2. **Corrigir parâmetros de autores**
   - Modo "All 13": passar lista completa
   - Modo "Dialogue Only": passar `--authors dialogue`

3. **Adicionar validação de PDF**
   - Confirmar arquivo antes de processar
   - Mostrar preview das informações

### Prioridade MÉDIA

4. **Melhorar feedback visual**
   - Notificações durante análise
   - Link para HTML no final
   - Estimativa de tempo restante

5. **Adicionar modo de recuperação**
   - Se análise falhar, permitir retry
   - Salvar progresso parcial

### Prioridade BAIXA

6. **Interface melhorada**
   - Preview do PDF selecionado
   - Histórico de análises
   - Comparação entre autores

---

## 🎯 SOLUÇÃO PROPOSTA

### Script Corrigido (v5.0)

```bash
#!/bin/bash
#
# 🎬 Scripturemon - Professional Screenplay Analyzer v5.0
# FASE 3 Compatible: Deep Context + Personalized Prompts
#

set -euo pipefail

readonly SCRIPTUREMON_DIR="/Users/clubproducoes/Digimundo/scripturemon"
readonly REQUIRED_MODEL="scripturemon-optimized"
readonly APP_NAME="Scripturemon v5.0"

# All 13 authors
readonly ALL_AUTHORS="aristotle campbell cowgill dialogue egri field mckee mckee_character mckee_dialogue seger snyder truby vogler"

validate_pdf() {
    local pdf_file="$1"

    if [ ! -f "$pdf_file" ]; then
        error_exit "PDF not found: $pdf_file"
    fi

    local size=$(du -h "$pdf_file" | cut -f1)
    local modified=$(stat -f %Sm "$pdf_file")

    # Show confirmation dialog
    osascript << EOF
tell application "System Events"
    activate
    display dialog "📄 CONFIRM SCREENPLAY\n\nFile: $(basename "$pdf_file")\nSize: $size\nModified: $modified\n\nProceed with analysis?" buttons {"Cancel", "Confirm"} default button 2 with title "$APP_NAME"
end tell
EOF
}

start_new_analysis() {
    local screenplay_file="$1"
    local analysis_mode="$2"

    # Validate PDF
    if ! validate_pdf "$screenplay_file"; then
        exit 0
    fi

    # Determine authors
    local authors_list=""
    if [ "$analysis_mode" = "All 13" ]; then
        authors_list="$ALL_AUTHORS"
    else
        authors_list="dialogue"
    fi

    notify "Starting Analysis" "FASE 3 System Active"

    # ✅ CORRETO: Use analyze.py with FASE 3 parameters
    osascript << EOF
tell application "Terminal"
    activate
    do script "cd '$SCRIPTUREMON_DIR' && python3 -u analyze.py '$screenplay_file' --authors $authors_list --deep --use-personalized-prompts"
end tell
EOF

    notify "Analysis Started" "Check Terminal for progress"
}

main() {
    validate_environment

    if check_existing_sessions; then
        exit 0
    fi

    local screenplay_file=$(get_screenplay_file "${1:-}")

    if [ -z "$screenplay_file" ]; then
        exit 0
    fi

    local analysis_mode=$(choose_analysis_mode)

    if [ "$analysis_mode" = "Cancel" ] || [ -z "$analysis_mode" ]; then
        exit 0
    fi

    start_new_analysis "$screenplay_file" "$analysis_mode"
}

main "$@"
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

Antes de usar o app, verificar:

- [ ] App chama `analyze.py` (não `analyze_with_checkpoints.py`)
- [ ] Flag `--use-personalized-prompts` está presente
- [ ] Flag `--deep` está presente
- [ ] Parâmetro `--authors` é especificado corretamente
- [ ] PDF é validado antes da análise
- [ ] Notificações funcionam
- [ ] Terminal abre com análise iniciada
- [ ] Outputs vão para `workspace/outputs/`

---

## 📝 TESTES NECESSÁRIOS

### Teste 1: Modo Dialogue Only
```bash
# Executar app
# Selecionar "Te Encontro em Mim .pdf"
# Escolher "Dialogue Only"
# Verificar:
- [ ] Terminal abre
- [ ] Comando correto: analyze.py ... --authors dialogue --deep --use-personalized-prompts
- [ ] Análise completa em ~6 minutos
- [ ] HTML gerado com 15-17KB
- [ ] Score real 16.0/10
```

### Teste 2: Modo All 13
```bash
# Executar app
# Selecionar "Te Encontro em Mim .pdf"
# Escolher "All 13"
# Verificar:
- [ ] Terminal abre
- [ ] Comando correto com todos os 13 autores
- [ ] Análise completa em ~90 minutos (13 x 7min)
- [ ] 13 HTMLs individuais gerados
- [ ] 1 HTML consolidado gerado
- [ ] Todos com scores 15.5-18.0/10
```

### Teste 3: Validação de PDF
```bash
# Executar app
# Selecionar PDF
# Verificar:
- [ ] Dialog mostra nome correto do arquivo
- [ ] Tamanho está correto
- [ ] Data de modificação está correta
- [ ] Pode cancelar antes da análise
```

---

## 🚀 IMPLEMENTAÇÃO

Para atualizar o app:

```bash
# 1. Backup do app atual
cp "/Applications/Analyze Screenplay.app/Contents/MacOS/run" \
   "/Applications/Analyze Screenplay.app/Contents/MacOS/run.backup_$(date +%Y%m%d_%H%M%S)"

# 2. Substituir com script correto v5.0
# (usar script da seção "Solução Proposta")

# 3. Dar permissão de execução
chmod +x "/Applications/Analyze Screenplay.app/Contents/MacOS/run"

# 4. Testar
open -a "Analyze Screenplay" "/Users/clubproducoes/Digimundo/scripturemon/inputs/examples/Te Encontro em Mim .pdf"
```

---

## 📊 IMPACTO ESPERADO

Após correção:

✅ **Qualidade**: 6-7/10 → 15.5-18.0/10 (+150%)
✅ **Tamanho**: 7-12KB → 15-22KB (+100%)
✅ **Confiabilidade**: App alinhado com sistema
✅ **Usabilidade**: Validação de PDF antes de processar
✅ **Feedback**: Notificações durante análise

---

**Status**: 🔴 Aguardando Implementação
**Prioridade**: 🚨 CRÍTICA
**Tempo estimado**: 30 minutos para implementar e testar
