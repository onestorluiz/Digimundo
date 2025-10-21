# 📚 Specialist: {{SPECIALIST_NAME}}

**Author Base**: {{AUTHOR_NAME}}
**Focus Area**: {{FOCUS_AREA}}
**Status**: {{STATUS}}
**Creation Date**: {{DATE}}

---

## 🎯 Purpose

This specialist provides in-depth screenplay analysis based on {{AUTHOR_NAME}}'s methodology for {{FOCUS_AREA}}.

### Key Features

- Deep context from {{AUTHOR_NAME}}'s theory book
- Specialized prompts using author's terminology
- Validation against author's quality criteria
- Concrete rewrites following author's principles

---

## 📖 Theory Base

**Book**: `theory/{{THEORY_BOOK_FILENAME}}`
**Key Concepts**:
- [Concept 1 from {{AUTHOR_NAME}}]
- [Concept 2 from {{AUTHOR_NAME}}]
- [Concept 3 from {{AUTHOR_NAME}}]

---

## ✅ Validation Criteria

This specialist validates analyses against the following criteria:

1. **Minimum Length**: 15,000+ characters
2. **Scenes Analyzed**: 3+ scenes in depth
3. **Quotes Included**: 3+ direct quotes from screenplay
4. **Rewrites Proposed**: 2+ concrete rewrite proposals
5. **Theory Citations**: 3+ explicit citations of {{AUTHOR_NAME}}'s concepts

**Passing Score**: >= 7.0/10

---

## 🚀 Usage

### Basic Usage

```python
from engine.specialists.{{SPECIALIST_NAME}}.specialist import {{SPECIALIST_CLASS_NAME}}

# Initialize specialist
specialist = {{SPECIALIST_CLASS_NAME}}(
    llm_model="scripturemon-optimized",
    deep_context=True
)

# Analyze screenplay
result = specialist.analyze_screenplay(
    screenplay_text=screenplay_content,
    screenplay_metadata={"title": "Example", "author": "John Doe"}
)

# Check results
print(f"Score: {result['validation']['score']}/10")
print(f"Passed: {result['validation']['passed']}")
```

### Via analyze.py

```bash
python3 analyze.py "path/to/screenplay.pdf" \
    --specialist {{SPECIALIST_NAME}} \
    --deep
```

---

## 📊 Expected Performance

**Typical Scores**: {{EXPECTED_SCORE_RANGE}}/10
**Analysis Time**: {{EXPECTED_TIME}} minutes
**Output Size**: {{EXPECTED_OUTPUT_SIZE}}KB

---

## 🔧 Quirks & Known Behaviors

### Quirks

- [Document any peculiar behaviors discovered during testing]
- [Example: "Tends to be more strict on dialogue in action scenes"]

### Strengths

- [What this specialist does particularly well]
- [Example: "Excellent at identifying subtext issues"]

### Limitations

- [Known limitations]
- [Example: "May struggle with non-traditional dialogue structures"]

---

## 📝 Example Output

### Sample Analysis Excerpt

```
### CENA 3 - Confronto no Restaurante

**Localização no roteiro**: Página 15, linha 12-28

**Problemas Identificados**:
1. Diálogo "on the nose" - viola princípio de [CONCEITO DO AUTOR]
2. Falta de subtexto - personagens dizem exatamente o que sentem

**Análise Detalhada**:
Segundo {{AUTHOR_NAME}}, diálogo efetivo deve [explicação do conceito]...

**Exemplo Original**:
```
MARIA
Eu estou com raiva de você!
```

**Proposta de Rewrite**:
```
MARIA
(olha para o prato, voz baixa)
A comida esfriou.
```

**Justificativa**:
Aplicando o princípio de [CONCEITO], o rewrite...
```

---

## 🧪 Testing

### Run Unit Tests

```bash
python3 tests/test_{{SPECIALIST_NAME}}.py
```

### Validate Specialist

```bash
cd specialist_factory
python3 validate_specialist.py {{SPECIALIST_NAME}}
```

---

## 📚 References

- {{AUTHOR_NAME}}. *[Book Title]*. [Publisher, Year]
- [Additional references if applicable]

---

## 🔄 Version History

### v1.0 ({{DATE}})
- Initial creation
- Deep context integration
- Core analysis functionality

---

**Last Updated**: {{DATE}}
**Status**: {{STATUS}}

**DIGIMUNDO PRESENTE 🥷**
