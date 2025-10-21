# 🏗️ ARQUITETURA DO SISTEMA - 24 Especialistas

**Data**: 10 de Outubro 2025
**Versão**: 1.0
**Status**: ✅ Documentado e Pronto

---

## 🎯 Conceito Central

### Como Funciona

**Cada especialista**:
- ✅ Foca em **1 ASPECTO** narrativo (dialogue, character, structure, pacing, etc.)
- ✅ Consulta **TODOS os 13 livros de teoria** internamente
- ✅ Usa **deep context queries** específicas para extrair conceitos relevantes
- ✅ Combina sabedoria de TODOS os autores focada no seu aspecto

---

## 📚 Os 13 Livros de Teoria

Cada especialista consulta internamente:

1. **Aristotle** - Poetics
2. **Campbell** - Hero with a Thousand Faces
3. **Cowgill** - (Específico)
4. **Egri** - Art of Dramatic Writing
5. **Field** - Screenplay
6. **McKee** - Story
7. **McKee** - Character
8. **McKee** - Dialogue
9. **Seger** - Making a Good Script Great
10. **Snyder** - Save the Cat
11. **Truby** - Anatomy of Story
12. **Vogler** - Writer's Journey
13. **outro** - (A confirmar)

---

## 🔍 Exemplo Concreto: DrDialogue

### Como DrDialogue Funciona

**Aspecto**: Dialogue Analysis

**Processo**:
1. **Recebe roteiro** para analisar
2. **Consulta interna** aos 13 livros com queries específicas:
   ```
   - McKee/Story Ch.17 → Extrai: "Subtext", "Dialogue as Action", "Text beneath text"
   - Truby/Anatomy Ch.10 → Extrai: "Moral Dialogue", "Values through speech"
   - Field/Screenplay Ch.12 → Extrai: "Functional dialogue", "Moves story forward"
   - Snyder/Save the Cat → Extrai: "Avoiding on-the-nose", "Realistic dialogue"
   - Aristotle/Poetics → Extrai: "Diction", "Speech reveals character"
   (... + outros 8 autores)
   ```
3. **Sintetiza conceitos** de todos os autores focados em DIALOGUE
4. **Analisa roteiro** aplicando essa sabedoria combinada
5. **Gera análise profunda** com citações e técnicas específicas

**Resultado**: Análise de diálogo usando sabedoria de 13 autores, não apenas 1

---

## 🎭 Exemplo Concreto: DrCharacter (A Criar)

### Como DrCharacter Funcionará

**Aspecto**: Character Analysis

**Processo**:
1. **Recebe roteiro** para analisar
2. **Consulta interna** aos 13 livros com queries específicas:
   ```
   - McKee/Story Ch.6 → Extrai: "True Character", "Character Arc", "Dimension"
   - Truby/Anatomy Ch.3 → Extrai: "Weakness/Need", "Ghost", "Desire Line"
   - Field/Screenplay Ch.4 → Extrai: "Three Dimensions", "Character Biography"
   - Snyder/Save the Cat → Extrai: "Transformation Machine", "Save the Cat moment"
   - Vogler/Writer's Journey → Extrai: "Archetypes", "Hero pattern"
   - Campbell/Hero 1000 → Extrai: "Hero transformation", "Supernatural aid"
   - Aristotle/Poetics Ch.13 → Extrai: "Hamartia", "Tragic hero"
   (... + outros 6 autores)
   ```
3. **Sintetiza conceitos** de todos os autores focados em CHARACTER
4. **Analisa roteiro** aplicando essa sabedoria combinada
5. **Gera análise profunda** de personagens

**Resultado**: Análise de personagem usando sabedoria de 13 autores

---

## 📊 Diferença Chave

### ❌ O Que NÃO É

```
Sistema de 13 especialistas:
  - Especialista McKee (analisa tudo pela perspectiva de McKee)
  - Especialista Truby (analisa tudo pela perspectiva de Truby)
  - Especialista Field (analisa tudo pela perspectiva de Field)
  - ... (13 análises completas, 1 por autor)

Resultado: 13 análises gerais, cada uma focada em 1 autor
```

### ✅ O Que É

```
Sistema de 24 especialistas:
  - DrDialogue (consulta os 13 autores para conceitos de DIALOGUE)
  - DrCharacter (consulta os 13 autores para conceitos de CHARACTER)
  - DrStructure (consulta os 13 autores para conceitos de STRUCTURE)
  - DrPacing (consulta os 13 autores para conceitos de PACING)
  - ... (24 análises focadas, cada uma consultando 13 autores)

Resultado: 24 análises específicas, cada uma usando sabedoria de 13 autores
```

---

## 🔧 Arquitetura Técnica

### Deep Context System

```python
class DrDialogue:
    def __init__(self):
        self.aspect = "dialogue"
        self.theory_books = load_all_13_books()

        self.deep_context_queries = [
            "McKee's concepts about dialogue and subtext",
            "Truby's moral dialogue techniques",
            "Field's functional dialogue principles",
            "Snyder's realistic dialogue guidelines",
            "Aristotle's diction concepts",
            # ... queries para todos os 13 autores
        ]

    def analyze(self, screenplay):
        # 1. Extrai conceitos relevantes dos 13 livros
        relevant_concepts = self.extract_from_theory(
            books=self.theory_books,
            queries=self.deep_context_queries
        )

        # 2. Sintetiza sabedoria focada em dialogue
        dialogue_wisdom = self.synthesize(relevant_concepts)

        # 3. Analisa roteiro com essa sabedoria
        analysis = self.deep_analyze(
            screenplay=screenplay,
            wisdom=dialogue_wisdom
        )

        return analysis
```

### Por Que Funciona Melhor

**Vantagens**:
- ✅ **Foco preciso**: Cada especialista é expert em 1 aspecto
- ✅ **Profundidade máxima**: Usa TODOS os autores para cada aspecto
- ✅ **Sem redundância**: 24 análises específicas vs 13 análises gerais
- ✅ **Cobertura completa**: 24 aspectos cobrem tudo
- ✅ **Qualidade consistente**: Cada aspecto tem sabedoria de 13 autores

**vs. Sistema por Autor**:
- ❌ Redundância: 13 análises gerais repetem conceitos
- ❌ Falta foco: Cada autor cobre tudo superficialmente
- ❌ Gaps: Alguns aspectos não bem cobertos por alguns autores

---

## 📋 Os 24 Especialistas

### 🔥 Core (3) - Prioridade Máxima
1. **DrDialogue** ✅ - Análise de diálogo
2. **DrCharacter** 📝 - Análise de personagem
3. **DrStructure** 📝 - Estrutura narrativa

### 🎬 Narrative (4)
4. **DrPacing** 📝 - Ritmo narrativo
5. **DrTheme** 📝 - Análise temática
6. **DrAction** 📝 - Sequências de ação
7. **DrConflict** 📝 - Análise de conflito

### ⚡ Tension (4)
8. **DrTension** 📝 - Construção de tensão
9. **DrSubtext** 📝 - Análise de subtexto
10. **DrExposition** 📝 - Exposição eficaz
11. **DrTransitions** 📝 - Transições entre cenas

### 🌟 Arc (3)
12. **DrOpening** 📝 - Abertura eficaz
13. **DrClimax** 📝 - Clímax impactante
14. **DrResolution** 📝 - Resolução satisfatória

### 🌍 World (3)
15. **DrWorldbuilding** 📝 - Construção de mundo
16. **DrStakes** 📝 - Stakes dramáticas
17. **DrMotivation** 📝 - Motivação de personagens

### 🔮 Deep (4)
18. **DrBackstory** 📝 - Backstory eficaz
19. **DrForeshadowing** 📝 - Foreshadowing sutil
20. **DrTwist** 📝 - Plot twists
21. **DrSymbolism** 📝 - Simbolismo

### 🎨 Meta (3)
22. **DrTone** 📝 - Tom narrativo
23. **DrGenre** 📝 - Convenções de gênero
24. **DrEvaluator** 📝 - Avaliação final

---

## 🚀 Processo de Análise

### Workflow Completo

```
1. Usuário submete roteiro
   ↓
2. Sistema roda 24 especialistas
   ↓
3. Cada especialista:
   a) Consulta 13 livros (deep context queries específicas)
   b) Extrai conceitos relevantes para seu aspecto
   c) Sintetiza sabedoria
   d) Analisa roteiro
   e) Gera análise focada
   ↓
4. Sistema consolida 24 análises
   ↓
5. Gera relatório final completo
```

### Tempo Estimado

- **1 especialista**: 5-7 minutos
- **24 especialistas**: 120-180 minutos (2-3 horas)
- **Paralelo possível**: Pode reduzir para 30-45 min se rodar múltiplos em paralelo

### Output Esperado

```
Roteiro: "Te Encontro em Mim.pdf"

Análises geradas:
  ✓ DrDialogue: 18KB (score 8.2/10)
  ✓ DrCharacter: 19KB (score 8.5/10)
  ✓ DrStructure: 17KB (score 7.8/10)
  ✓ DrPacing: 16KB (score 8.0/10)
  ... (24 análises no total)

Relatório final: 450KB
Qualidade média: 8.1/10
Tempo total: 145 minutos
```

---

## 🎯 Próximos Passos

### Fase 1: Core Trio (Semana 1)
- [x] DrDialogue (já criado)
- [ ] DrCharacter
- [ ] DrStructure

### Fase 2-5: Restantes 21
- Ver `MEMORIA_ESPECIALISTAS.md` para lista completa e prioridades

### Ferramentas
- ✅ `specialist_factory/` - Sistema de criação pronto
- ✅ `BLUEPRINT_SPECIALIST.md` - Guia completo
- ✅ `CHECKLIST_CRIACAO.md` - Passo-a-passo
- ✅ `validate_specialist.py` - Validação automática

---

## 📖 Documentação Relacionada

- `MEMORIA_ESPECIALISTAS.md` - Histórico e lista completa dos 24
- `LISTA_ESPECIALISTAS_ALVO.md` - Mapeamento detalhado com modelfiles
- `BLUEPRINT_SPECIALIST.md` - Como criar cada especialista
- `CHECKLIST_CRIACAO.md` - Checklist de criação
- `README.md` - Visão geral do specialist_factory

---

**Última Atualização**: 10 de Outubro 2025, 18:30
**Status**: ✅ Arquitetura Documentada e Validada

**DIGIMUNDO PRESENTE 🥷**

---

## 💡 Perguntas Frequentes

**P: Por que 24 especialistas e não 13?**
R: 24 aspectos narrativos vs 13 autores. Melhor ter expert em "dialogue" consultando 13 autores do que ter expert em "McKee" analisando tudo.

**P: Cada especialista precisa dos 13 livros?**
R: Sim, mas usa deep context queries específicas. DrDialogue só extrai conceitos de DIALOGUE, DrCharacter só de CHARACTER, etc.

**P: Qual a vantagem sobre sistema anterior?**
R: Foco + Profundidade. Análise específica de dialogue usando 13 autores > análise geral usando 1 autor.

**P: Quanto tempo demora criar os 23 restantes?**
R: ~30-45 min por especialista = 15-20 horas total (dividido em sessões).

**P: Sistema está pronto?**
R: Sim! specialist_factory completo, templates prontos, validação automática funcionando.
