# 🔥🔥🔥 DIFF GUIDE - O QUE MUDA POR SPECIALIST 🔥🔥🔥

**Data:** 2025-10-05 (Atualizado: 05/10/2025 08:16)
**Versão:** 2.0 (Atualizado com 4 livros de estrutura)
**Uso:** Guia de transformação de DrDialogue para outros specialists
**📍 Localização:** `/Users/clubproducoes/Digimundo/claude_code/MEMORY/conhecimentos/🔥🔥🔥DIFF_GUIDE_POR_SPECIALIST🔥🔥🔥.md`

---

## 🔥 AVANÇO VERSÃO 2.0 - DrStructure Implementado

**Status:** ✅ DrStructure criado e validado com 4 livros de teoria
**Arquivos:**
- 📍 `/Users/clubproducoes/Digimundo/scripturemon-clean/specialists/dual_core/base/dr_structure.py`
- 📍 `/Users/clubproducoes/Digimundo/scripturemon-clean/specialists/rules/structure_rules.yaml`
- 📍 `/Users/clubproducoes/Digimundo/scripturemon-clean/core/theory_indexer.py` (linhas 691, 853-858, 708-710)

**Teoria carregada:**
1. Making a Good Script Great (Seger) - 251 chunks
2. Story (McKee) - 302 chunks
3. Screenplay (Field) - 251 chunks
4. Save the Cat (Snyder) - 137 chunks
**Total:** 874 chunks, 392,240 palavras

---

## 📍 VOCÊ ESTÁ AQUI

```
1. ✅ COMPLETO: TEMPLATE_MASTER_DrDialogue_ANOTADO.py
2. ✅ COMPLETO: CHECKLIST_NOVO_SPECIALIST.md
3. ✅ VOCÊ ESTÁ AQUI: DIFF_GUIDE_POR_SPECIALIST.md
4. ✅ COMPLETO: DrStructure implementado e validado
5. ⏭️  PRÓXIMO: validate_specialist.py
```

---

## 🎯 COMO USAR ESTE GUIA

1. Escolha o specialist que quer criar (ex: DrStructure)
2. Vá para a seção correspondente abaixo
3. Siga a tabela de transformações
4. Use CTRL+F para encontrar no template e substituir

---

## 📊 TABELA GERAL: O QUE MUDA vs O QUE NUNCA MUDA

| Aspecto | MUDA | NUNCA MUDA |
|---------|------|------------|
| **Nome da classe** | ✅ DrDialogue → DrStructure | ❌ Estrutura de classe |
| **Identidade** | ✅ name, title, specialty | ❌ Campos (name, title, specialty) |
| **Patterns** | ✅ exposition_markers → plot_points | ❌ Bilíngue (EN + PT) |
| **Dataclasses** | ✅ DialogueAnalysis → StructureAnalysis | ❌ Número mínimo (2) |
| **Métodos análise** | ✅ _analyze_subtext → _analyze_acts | ❌ Retornar float/dict/list |
| **Score base** | ❌ | ✅ Sempre 90.0 |
| **Penalties** | ❌ | ✅ Sempre 20/15/8/5 |
| **Range** | ❌ | ✅ Sempre 5-95 |
| **Output dict** | ✅ Métricas específicas | ❌ Chaves obrigatórias |
| **YAML file** | ✅ Nome do arquivo | ❌ Estrutura (id, title, severity, etc) |

---

## 🏗️ DR STRUCTURE (Análise de Estrutura)

### Transformações Principais

| DrDialogue (ORIGEM) | DrStructure (DESTINO) |
|---------------------|----------------------|
| **CLASSE** |
| `class DrDialogue` | `class DrStructure` |
| `class DrCharacterDialogue` | `class DrCharacterStructure` |
| **IDENTIDADE** |
| `name = "Script Doctor Dialoguemon"` | `name = "Script Doctor Structuremon"` |
| `digimon_name = "Dialoguemon"` | `digimon_name = "Structuremon"` |
| `title = "...Dialogue and Voice Specialist"` | `title = "...Three-Act Structure Specialist"` |
| `specialty = "Dialogue authenticity, character voice..."` | `specialty = "Three-act structure, plot points, paradigm..."` |
| **YAML PATH** |
| `character_dialogue_rules.yaml` | `structure_rules.yaml` |
| **DATACLASSES** |
| `@dataclass DialogueAnalysis` | `@dataclass StructureAnalysis` |
| `character: str` | `scene_number: int` |
| `line: str` | `description: str` |
| `has_subtext: bool` | `has_turning_point: bool` |
| `emotional_tone: str` | `act_type: str  # I, II, III` |
| `@dataclass CharacterVoice` | `@dataclass ActStructure` |
| `name: str` | `act_number: int` |
| `total_lines: int` | `total_scenes: int` |
| `distinctiveness_score: float` | `coherence_score: float` |
| **PATTERNS** |
| `self.exposition_markers = [...]` | `self.act_markers = ["INT.", "EXT.", "FADE IN", "FADE OUT", ...]` |
| `self.on_the_nose_phrases = [...]` | `self.paradigm_keywords = ["inciting incident", "midpoint", "climax", ...]` |
| `self.cliche_phrases = [...]` | `self.structure_cliches = ["deus ex machina", "rushed ending", ...]` |
| **MÉTODOS EXTRAÇÃO** |
| `def _extract_dialogue(...)` | `def _extract_acts(...)` |
| `def _analyze_single_dialogue(...)` | `def _analyze_single_scene(...)` |
| **MÉTODOS ANÁLISE** |
| `def _analyze_authenticity(...)` | `def _analyze_paradigm_adherence(...)` |
| `def _analyze_voice_distinctiveness(...)` | `def _analyze_act_proportions(...)` |
| `def _analyze_subtext(...)` | `def _analyze_plot_points(...)` |
| `def _detect_exposition_dumps(...)` | `def _detect_missing_beats(...)` |
| `def _analyze_dialogue_purpose(...)` | `def _analyze_structural_purpose(...)` |
| `def _analyze_natural_flow(...)` | `def _analyze_pacing_flow(...)` |
| `def _detect_cliches(...)` | `def _detect_structural_cliches(...)` |
| `def _analyze_dialogue_conflict(...)` | `def _analyze_turning_points(...)` |
| **BUILD PROFILES** |
| `def _build_voice_profiles(...)` | `def _build_act_summaries(...)` |
| **MÉTODOS INVARIÁVEIS** (NÃO MUDAR NOMES) |
| `def _check_dialogue_rules(...)` | `def _check_structure_rules(...)` |
| `def _calculate_dialogue_score(...)` | `def _calculate_structure_score(...)` |
| `def _generate_diagnosis(...)` | `def _generate_diagnosis(...)` ← IGUAL |
| `def _generate_recommendations(...)` | `def _generate_recommendations(...)` ← IGUAL |
| **OUTPUT DICT** |
| `"total_dialogue_lines": len(...)` | `"total_scenes": len(...)` |
| `"character_count": len(...)` | `"total_acts": 3` |
| `"voice_profiles": [...]` | `"act_summaries": [...]` |
| `"authenticity_score": ...` | `"paradigm_score": ...` |
| `"subtext_score": ...` | `"plot_points_score": ...` |
| `"on_the_nose_count": ...` | `"missing_beats": ...` |

### Exemplo de YAML (`structure_rules.yaml`)

**📍 Localização:** `/Users/clubproducoes/Digimundo/scripturemon-clean/specialists/rules/structure_rules.yaml`

```yaml
domain: structure
specialist: "Script Doctor Structuremon"
digimon_name: "Structuremon"
title: "Script Doctor - Three-Act Structure Specialist"
specialty: "Three-act structure, plot points, paradigm, act proportions"

# 🔥 TEORIA: 4 livros carregados (Seger PRIMARY, McKee, Field, Snyder)
# Mapeado em theory_indexer.py linhas 853-858

rules:
  - id: STRUCT.R001
    title: "Three-Act Structure Present"
    category: "Paradigm"
    severity: "critical"
    test: "Does screenplay follow three-act structure?"
    fail_msg: "Missing clear three-act structure"
    fix: "Establish Act I (setup), Act II (confrontation), Act III (resolution)"
    # Teoria: Seger (act two: 95), McKee, Field (structure: 73)

  - id: STRUCT.R002
    title: "Inciting Incident Present"
    category: "Plot Points"
    severity: "critical"
    test: "Is there an inciting incident around page 10-15?"
    fail_msg: "Missing or delayed inciting incident"
    fix: "Place inciting incident within first 10-15 pages"
    # Teoria: McKee (inciting incident: 121), Seger (catalyst: 68)

  - id: STRUCT.R003
    title: "Midpoint Present"
    category: "Plot Points"
    severity: "high"
    test: "Is there a clear midpoint around page 50-60?"
    fail_msg: "Missing or unclear midpoint"
    fix: "Create a midpoint that shifts story direction"
    # Teoria: Snyder (midpoint: 46), Seger

  - id: STRUCT.R004
    title: "Act Proportions Correct"
    category: "Paradigm"
    severity: "high"
    test: "Are acts proportioned roughly 25/50/25?"
    fail_msg: "Acts are disproportionate"
    fix: "Rebalance acts to 25% / 50% / 25% split"
    # Teoria: Field (paradigm: 35), Seger, McKee

  - id: STRUCT.R005
    title: "Plot Point 1 Present"
    category: "Plot Points"
    severity: "critical"
    test: "Is Plot Point 1 around page 25-30?"
    fail_msg: "Missing or misplaced Plot Point 1"
    fix: "Place Plot Point 1 at end of Act I (page 25-30)"
    # Teoria: Field, Seger (turning point: 103), McKee
```

### Validação DrStructure (05/10/2025)

**Test executado:** `test_integration_complete.py`
**Resultado:**
- ✅ 4 books loaded (was 2)
- ✅ 874 chunks (was 439) - +99%
- ✅ 392,240 words (was 196,919) - +99%
- ✅ LLM insights: 4,063 chars (was 2,907) - +40%
- ✅ Authors cited: Seger + McKee + Field
- ✅ HTML output: 11,072 bytes
- ✅ Score: 90.0/100

---

## ⏱️ DR PACING (Análise de Ritmo)

### Transformações Principais

| DrDialogue (ORIGEM) | DrPacing (DESTINO) |
|---------------------|-------------------|
| **CLASSE** |
| `class DrDialogue` | `class DrPacing` |
| **IDENTIDADE** |
| `name = "Script Doctor Dialoguemon"` | `name = "Script Doctor Pacingmon"` |
| `specialty = "Dialogue authenticity..."` | `specialty = "Pacing, rhythm, tempo, scene beats..."` |
| **YAML** |
| `character_dialogue_rules.yaml` | `pacing_rules.yaml` |
| **DATACLASSES** |
| `@dataclass DialogueAnalysis` | `@dataclass BeatAnalysis` |
| `character: str` | `scene_id: str` |
| `line: str` | `beat_description: str` |
| `word_count: int` | `duration_seconds: float` |
| `@dataclass CharacterVoice` | `@dataclass SequenceRhythm` |
| **PATTERNS** |
| `self.exposition_markers` | `self.pacing_indicators = ["action", "dialogue", "montage", "pause", ...]` |
| `self.on_the_nose_phrases` | `self.tempo_markers = ["fast", "slow", "builds", "suspense", ...]` |
| **MÉTODOS** |
| `def _extract_dialogue(...)` | `def _extract_beats(...)` |
| `def _analyze_authenticity(...)` | `def _analyze_tempo(...)` |
| `def _analyze_subtext(...)` | `def _analyze_rhythm_variation(...)` |
| `def _detect_exposition_dumps(...)` | `def _detect_pacing_lulls(...)` |
| **OUTPUT** |
| `"total_dialogue_lines": ...` | `"total_beats": ...` |
| `"authenticity_score": ...` | `"tempo_score": ...` |
| `"subtext_score": ...` | `"rhythm_variation": ...` |

### Exemplo de YAML (`pacing_rules.yaml`)

```yaml
rules:
  - id: PACE.R001
    title: "Varied Pacing"
    severity: "high"
    test: "Does pacing vary between fast and slow?"
    fail_msg: "Monotonous pacing throughout"
    fix: "Alternate between action beats and quiet moments"

  - id: PACE.R002
    title: "No Extended Lulls"
    severity: "medium"
    test: "Are there sections without tension for >10 minutes?"
    fail_msg: "Extended lulls in tension"
    fix: "Inject conflict or urgency every 10 minutes"
```

---

## 👥 DR CHARACTER PSYCHOLOGY (Análise de Psicologia)

### Transformações Principais

| DrDialogue (ORIGEM) | DrCharacterPsychology (DESTINO) |
|---------------------|--------------------------------|
| **CLASSE** |
| `class DrDialogue` | `class DrCharacterPsychology` |
| **YAML** |
| `character_dialogue_rules.yaml` | `character_psychology_rules.yaml` |
| **DATACLASSES** |
| `@dataclass DialogueAnalysis` | `@dataclass CharacterMomentAnalysis` |
| `@dataclass CharacterVoice` | `@dataclass PsychologicalProfile` |
| **PATTERNS** |
| `self.exposition_markers` | `self.motivation_markers = ["wants", "needs", "fears", ...]` |
| `self.on_the_nose_phrases` | `self.inconsistency_markers = ["out of character", "contradicts", ...]` |
| **MÉTODOS** |
| `def _analyze_authenticity(...)` | `def _analyze_consistency(...)` |
| `def _analyze_subtext(...)` | `def _analyze_internal_conflict(...)` |
| `def _build_voice_profiles(...)` | `def _build_psychological_profiles(...)` |

---

## 🎬 TEMPLATE GENÉRICO (Para Qualquer Specialist)

Use este template quando criar specialist NOVO (não listado acima):

### Passo 1: Defina a Essência

```python
# O que este specialist analisa?
ANÁLISE: "_______________"  # Ex: Opening hooks, Visual motifs, etc

# Qual a unidade básica?
UNIDADE: "_______________"  # Ex: Opening scene, Visual element, etc

# Qual o agregado/profile?
AGREGADO: "_______________"  # Ex: Opening summary, Motif catalog, etc
```

### Passo 2: Transforme Nomes

```python
# CLASSE
DrDialogue → Dr{Nome}

# DATACLASSES
DialogueAnalysis → {Unidade}Analysis
CharacterVoice → {Agregado}Profile

# MÉTODOS
_extract_dialogue → _extract_{unidades}
_analyze_subtext → _analyze_{aspecto_principal}
_build_voice_profiles → _build_{agregado}_summaries
```

### Passo 3: Adapte Patterns

```python
# Substitua patterns de diálogo por patterns do specialist
self.exposition_markers → self.{tipo}_markers
# SEMPRE bilíngue (EN + PT)
```

### Passo 4: Mantenha INVARIÁVEL

```python
# NÃO MUDAR:
- Score base: 90.0
- Penalties: 20/15/8/5
- Range: 5-95
- Output format: dict com specialist, score, violations, diagnosis, recommendations, signature
- Métodos: _check_rules, _calculate_score, _generate_diagnosis, _generate_recommendations
```

---

## 📋 REFERÊNCIA RÁPIDA: MAPEAMENTO DE 22 SPECIALISTS

| Specialist | Unidade Básica | Agregado | Aspecto Principal |
|------------|----------------|----------|-------------------|
| Dialogue | Linha de diálogo | Voice profile | Authenticity, subtext |
| Structure | Cena/Ato | Act summary | Paradigm, plot points |
| Pacing | Beat | Sequence rhythm | Tempo, variation |
| Opening | Opening scene | Opening summary | Hook, setup |
| Climax | Climax scene | Climax structure | Stakes, payoff |
| Resolution | Final scene | Resolution summary | Closure, satisfaction |
| Transitions | Transição | Transition flow | Smoothness, logic |
| Psychology | Momento character | Psychological profile | Consistency, depth |
| Arcs | Checkpoint de arc | Arc trajectory | Transformation, growth |
| Relationships | Interação | Relationship map | Dynamics, development |
| Voice | Linha de diálogo | Voice distinctiveness | Uniqueness, consistency |
| Subtext | Linha/cena | Subtext layers | Implication, depth |
| Formatting | Linha de script | Format compliance | Industry standards |
| Action | Action line | Visual storytelling | Show don't tell |
| Symbolism | Símbolo/metáfora | Symbol catalog | Meaning, recurrence |
| Theme | Momento temático | Theme consistency | Exploration, depth |
| Tone | Cena | Tone profile | Mood, atmosphere |
| Visual Motifs | Motivo visual | Motif catalog | Recurrence, meaning |
| Genre | Momento de gênero | Genre adherence | Conventions, expectations |
| World Building | Elemento de mundo | World consistency | Rules, logic |
| Originality | Elemento | Uniqueness score | Fresh perspectives |
| Market Potential | Aspecto comercial | Market fit | Commercial viability |

---

## ✅ VALIDAÇÃO FINAL

Antes de considerar transformação completa:

- [ ] Todos os nomes transformados (classe, dataclasses, métodos)
- [ ] Patterns específicos do specialist definidos
- [ ] Patterns são bilíngues (EN + PT)
- [ ] YAML file criado com regras específicas
- [ ] Score calculation mantido (90 base, 20/15/8/5 penalties, 5-95 range)
- [ ] Output dict tem chaves obrigatórias
- [ ] Métodos invariáveis não foram alterados (estrutura)

---

## 📚 PRÓXIMOS PASSOS

```
1. ✅ COMPLETO: TEMPLATE_MASTER_DrDialogue_ANOTADO.py
2. ✅ COMPLETO: CHECKLIST_NOVO_SPECIALIST.md
3. ✅ COMPLETO: DIFF_GUIDE_POR_SPECIALIST.md (você está aqui)
4. ⏭️  PRÓXIMO: validate_specialist.py
   📍 Localização: /Users/clubproducoes/Digimundo/claude_code/MEMORY/conhecimentos/
   🎯 Ação: Rodar para validar specialist criado
```

---

**DIGIMUNDO PRESENTE 🥷**
