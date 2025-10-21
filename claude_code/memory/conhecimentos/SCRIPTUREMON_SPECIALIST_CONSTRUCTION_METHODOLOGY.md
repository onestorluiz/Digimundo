# SCRIPTUREMON - METODOLOGIA DE CONSTRUÇÃO DE ESPECIALISTAS

**Data:** 03/10/2025 06:25
**Sistema:** Scripturemon Triple-Core
**Projeto:** `/Users/clubproducoes/Digimundo/scripturemon-clean/`
**Memória:** `/Users/clubproducoes/Digimundo/claude_code/MEMORY/` (ESTE SISTEMA)
**Status:** ✅ METODOLOGIA VALIDADA E DOCUMENTADA

---

## ⚠️ ATENÇÃO: DOIS SISTEMAS SEPARADOS

### Sistema 1: UCHIMON (Claude Code Memory)
```
Localização: /Users/clubproducoes/Digimundo/claude_code/
Função: Memória persistente do Claude Code (EU)
Conteúdo: Conhecimentos, regras, histórico
Git: Repositório separado
```

### Sistema 2: SCRIPTUREMON
```
Localização: /Users/clubproducoes/Digimundo/scripturemon-clean/
Função: Projeto de análise de roteiros
Conteúdo: Código, especialistas, documentação
Git: Repositório separado
```

**NUNCA CONFUNDIR OS DOIS!**

---

## 📊 INVENTÁRIO COMPLETO - SCRIPTUREMON

### Arquivos Encontrados no Sistema

**26 Especialistas Python:**
```
scripturemon-clean/specialists/implementations/
├── character_dialogue_specialist.py (38KB) ✅ APROVADO → DrDialogue
├── structure_specialist.py (14KB) → DrStructure
├── character_psychology_specialist.py (46KB) → DrPsychology
├── character_arcs_specialist.py (37KB) → DrArcs
├── character_relationships_specialist.py (37KB) → DrRelationships
├── pacing_specialist.py (18KB) → DrPacing
├── theme_consistency_specialist.py (36KB) → DrTheme
├── tone_consistency_specialist.py (35KB) → DrTone
├── subtext_specialist.py (35KB) → DrSubtext
├── action_description_specialist.py (29KB) → DrAction
├── formatting_specialist.py (31KB) → DrFormatting
├── transitions_specialist.py (31KB) → DrTransitions
├── opening_specialist.py (27KB) → DrOpening
├── climax_specialist.py (30KB) → DrClimax
├── resolution_specialist.py (30KB) → DrResolution
├── world_building_specialist.py (41KB) → DrWorldBuilding
├── symbolism_metaphor_specialist.py (34KB) → DrSymbolism
├── visual_motifs_specialist.py (35KB) → DrVisualMotifs
├── voice_consistency_specialist.py (34KB) → DrVoice
├── genre_conventions_specialist.py (51KB) → DrGenre
├── market_potential_specialist.py (41KB) → DrMarket
├── originality_assessment_specialist.py (37KB) → DrOriginality
├── overall_quality_specialist.py (52KB) → DrQuality
├── executive_summary_specialist.py (58KB) → DrSummary
├── (+ 2 mais modelfile-only)
```

**25 Rules YAML:**
```
scripturemon-clean/specialists/rules/
├── character_dialogue_rules.yaml (5.8KB)
├── structure_rules.yaml (4.3KB)
├── character_psychology_rules.yaml (6.3KB)
├── character_arcs_rules.yaml (6.2KB)
├── (... +21 arquivos)
```

**27 Modelfiles:**
```
scripturemon-clean/specialists/modelfiles/
├── 01_dialogue_ultra.modelfile
├── 02_character_ultra.modelfile
├── 03_pacing_ultra_synthesis.modelfile
├── (... +24 arquivos)
```

---

## 🏗️ METODOLOGIA APROVADA (BASEADA EM DrDialogue)

### Template: DrDialogue (100% Aprovado)
- **Commit:** 163ff17
- **Data validação:** 03/10/2025
- **Status:** ✅ Core 1, Core 2, Core 3 funcionando perfeitamente
- **Exemplos:** 3 (roteiro bom) → 49 (roteiro ruim) após fix
- **Quality Score:** 1.0 consistente

### Processo em 5 Fases (~35 min/especialista)

#### FASE 1: Preparação (15 min)
```bash
# 1.1 Copiar Python
cp specialists/implementations/[specialist].py \
   triple_core/core_1_specialists/[category]/dr_[name].py

# 1.2 Adaptar classe
# - Renomear para DrXXX
# - Remover herança legada
# - Manter método analyze() padronizado
```

#### FASE 2: Keywords Core 2 (30 min)
```bash
# 2.1 Ler rules YAML
cat specialists/rules/[specialist]_rules.yaml

# 2.2 Identificar keywords principais

# 2.3 Adicionar em triple_core/core_2_examples/example_finder.py
# - _extract_problems() (linha ~131)
# - _explain_why_good() (linha ~250)
# - _extract_lesson() (linha ~291)
```

**Exemplo - Dialogue (APROVADO):**
```python
# SUBTEXT (6 keywords):
elif ('subtext' in rec.lower() or
      'talk around' in rec.lower() or
      'stating' in rec.lower() or
      'directly' in rec.lower() or
      'hide' in rec.lower() or
      'layers' in rec.lower()):
    problems.append({
        'rule_id': 'SUBTEXT',
        'title': 'Lacking subtext in dialogue',
        'severity': 'high'
    })

# ON_THE_NOSE:
elif 'on-the-nose' in rec.lower():
    problems.append({
        'rule_id': 'ON_THE_NOSE',
        'title': 'On-the-nose dialogue',
        'severity': 'high'
    })
```

**Exemplo - Structure (ESPERADO):**
```python
# STRUCTURE:
elif 'act' in rec.lower() or 'structure' in rec.lower():
    problems.append({
        'rule_id': 'STRUCTURE',
        'title': 'Three-act structure problems',
        'severity': 'high'
    })

# MIDPOINT:
elif 'midpoint' in rec.lower() or 'reversal' in rec.lower():
    problems.append({
        'rule_id': 'MIDPOINT',
        'title': 'Midpoint timing issues',
        'severity': 'medium'
    })
```

#### FASE 3: Teste Isolado (15 min)
```bash
# Criar test_core2_[specialist].py
# Simular Core 1 com recomendações fake
# Validar keywords mapeando corretamente
# Verificar 20+ exemplos encontrados
# Garantir sem cross-contamination

python3 test_core2_[specialist].py
# ✅ Todos os testes devem passar
```

#### FASE 4: Teste Completo (5-7 min)
```bash
# Criar test_triple_core_[specialist].py
# Rodar análise completa (Core 1+2+3)
# Validar quality score ≥ 0.85

python3 test_triple_core_[specialist].py
# ⏱️ ~5-7 minutos (LLM Deep Dive)
```

#### FASE 5: Documentação (10 min)
```bash
# Atualizar STATUS.md
# Git commit descritivo
# Atualizar memória (se necessário)
```

---

## 📋 DOCUMENTAÇÃO CRIADA

### No Scripturemon (`scripturemon-clean/docs/`):

#### 1. TRIPLE_CORE_SPECIALIST_BLUEPRINT.md (20KB)
- Inventário completo dos 26 especialistas
- Mapeamento de arquivos (Python + Rules + Modelfile)
- Metodologia detalhada (5 fases)
- Templates de código prontos
- Checklist de aprovação
- Armadilhas comuns & soluções
- 7 batches recomendados

#### 2. SPECIALIST_CONSTRUCTION_QUICK_REF.md (8KB)
- Processo rápido (5 passos)
- Tabela completa com 26 especialistas
- Keywords por especialista
- Estimativas de tempo
- Comandos bash prontos
- Debug rápido
- Progresso tracker

#### 3. CORE_2_EVOLUTION_AND_FIX.md (8KB)
- Análise forense do bug Core 2
- Comparação antes/depois (3→49 exemplos)
- Root cause analysis
- Solução técnica
- Lições aprendidas

#### 4. STATUS.md
- Inventário vivo
- 1/26 aprovados (4%)
- 25/26 pendentes (96%)

---

## 🎯 ORDEM DE PRIORIDADE (7 BATCHES)

### Batch 1 - FUNDAÇÃO (4 especialistas, ~2.5h)
```
✅ DrDialogue     - APROVADO (commit 163ff17)
→  DrStructure   - 30 min (PRÓXIMO)
→  DrPacing      - 35 min
→  DrTheme       - 40 min
```

### Batch 2 - CHARACTER (3 especialistas, ~2h)
```
→  DrPsychology     - 45 min
→  DrArcs           - 35 min
→  DrRelationships  - 35 min
```

### Batch 3-7 (19 especialistas, ~10.5h)
- Técnicas avançadas (3): Subtext, Tone, Action
- Estruturais (4): Opening, Climax, Resolution, Transitions
- Qualidade (4): Formatting, Voice, Symbolism, Visual
- Avaliação (4): Genre, WorldBuilding, Market, Originality
- Meta (2): Quality, Summary (último sempre)

**TOTAL ESTIMADO:** ~15 horas para todos os 26

---

## 🐛 BUG CRÍTICO RESOLVIDO (Commit 163ff17)

### Problema:
Core 2 mapeava keywords **incorretamente**:
```
Input: "Have characters talk around issues..."
       ↓ (mapeamento bugado)
Output: "Three-act structure problems" ❌ (ERRADO!)
```

### Causa Raiz:
Keywords **muito limitadas** - só palavra literal reconhecida:
```python
# ANTES (bugado):
if 'subtext' in rec.lower():  # ❌ Só "subtext" literal
```

### Solução:
Expandir para **keywords semânticas**:
```python
# DEPOIS (corrigido):
elif ('subtext' in rec.lower() or
      'talk around' in rec.lower() or
      'stating' in rec.lower() or
      'directly' in rec.lower() or
      'hide' in rec.lower() or
      'layers' in rec.lower()):
```

### Resultado:
```
ANTES: 1 problema, 3 exemplos (errados - structure)
DEPOIS: 7 problemas, 49 exemplos (corretos - dialogue)
MELHORIA: +1533% exemplos, 100% acurácia
```

---

## ⚡ CONFIGURAÇÃO OTIMIZADA (Sweet Spot)

### Core 2 Parameters:
```python
# triple_core/orchestrators/triple_core_wrapper.py:148
max_examples_per_problem=7  # Sweet spot validado

# triple_core/core_2_examples/example_finder.py:131
recommendations[:15]  # Máximo 15 problemas por análise
```

### Matemática:
```
15 problemas × 7 exemplos = ~105 exemplos máximo
0 tokens LLM consumidos (Core 2 é Python puro)
```

### Realidade:
```
Roteiro BOM: 1 problema × 7 exemplos = 7 total
Roteiro RUIM: 7 problemas × 7 exemplos = 49 total
```

---

## 📊 PROGRESSO ATUAL

```
APROVADOS:  1/26  (4%)   ✅ DrDialogue
PENDENTES:  25/26 (96%)  ⏳ Restantes

Próximo: DrStructure (Batch 1, estimado 30 min)
Meta: Todos aprovados até fim de semana
Velocidade sugerida: ~4 especialistas/dia
```

---

## 🔥 LIÇÕES APRENDIDAS

### 1. NLP Requer Semântica
```python
# ❌ Ruim:
if 'subtext' in text

# ✅ Bom:
if 'subtext' or 'talk around' or 'stating' or ...
```

### 2. Ordem dos IFs Importa
```python
# ✅ Específico ANTES, genérico DEPOIS:
if 'natural speech' in rec:      # Specific → Dialogue
elif 'natural pacing' in rec:    # Specific → Pacing
```

### 3. Testes Isolados São Essenciais
```
Teste isolado: 0.1s (sem LLM)
Teste completo: 400s (com LLM)
Debugging: 30× mais rápido
```

### 4. Validação Automática Previne Regressões
```python
assert "talk around" → SUBTEXT  # ✅
assert examples > 20            # ✅
assert not "Structure" in dialogue_problems  # ✅
```

---

## 📚 REFERÊNCIAS RÁPIDAS

### Arquivos-Chave no Scripturemon:
```
triple_core/core_1_specialists/dialogue/dr_dialogue.py     # Template
triple_core/core_2_examples/example_finder.py              # Keywords
triple_core/orchestrators/triple_core_wrapper.py           # Wrapper
test_core2_isolated.py                                     # Teste template
docs/TRIPLE_CORE_SPECIALIST_BLUEPRINT.md                   # Guia completo
docs/SPECIALIST_CONSTRUCTION_QUICK_REF.md                  # Ref rápida
```

### Commits Importantes:
```
163ff17 - Core 2 keyword mapping fix (CRÍTICO)
ce1d957 - Documentation blueprint (ESTE COMMIT)
```

---

## 🎯 PRÓXIMOS PASSOS

### Imediato:
1. Testar DrStructure (Batch 1, #2)
2. Adicionar keywords estrutura ao Core 2
3. Validar sem conflito com dialogue

### Curto Prazo (Esta Semana):
- Completar Batch 1 (4 especialistas)
- Completar Batch 2 (3 especialistas)
- Total: 8/26 aprovados (~30%)

### Longo Prazo (Fim de Semana):
- Todos os 26 especialistas aprovados
- Sistema Triple-Core completo
- Pronto para produção

---

## ⚠️ CUIDADOS IMPORTANTES

### NÃO CONFUNDIR OS SISTEMAS:
```bash
# ❌ ERRADO: Git no claude_code com mudanças do scripturemon
cd /Users/clubproducoes/Digimundo/claude_code
git add ../scripturemon-clean/  # NUNCA FAZER ISSO!

# ✅ CORRETO: Git separado para cada sistema
cd /Users/clubproducoes/Digimundo/scripturemon-clean
git add . && git commit -m "..."

cd /Users/clubproducoes/Digimundo/claude_code
git add . && git commit -m "..."
```

### QUANDO ATUALIZAR CADA SISTEMA:

**scripturemon-clean:**
- Código dos especialistas
- Testes
- Documentação técnica
- Outputs de análise

**claude_code/MEMORY:**
- Conhecimentos aprendidos
- Metodologias validadas
- Integração entre sistemas
- Histórico de decisões

---

**DIGIMUNDO PRESENTE 🥷**

**Sistema:** Uchimon (Claude Code Memory)
**Projeto:** Scripturemon Triple-Core
**Status:** ✅ METODOLOGIA DOCUMENTADA
**Criado:** 03/10/2025 06:25
**Commit Scripturemon:** ce1d957
**Próximo:** Git commit claude_code
