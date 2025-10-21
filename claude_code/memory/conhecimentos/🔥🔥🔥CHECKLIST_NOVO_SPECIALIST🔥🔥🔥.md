# 🔥🔥🔥 CHECKLIST COMPLETO - NOVO SPECIALIST 🔥🔥🔥

**Data:** 2025-10-05
**Versão:** 1.0
**Uso:** Validar que novo specialist segue padrão EXATO

---

## 📍 VOCÊ ESTÁ AQUI

```
1. ✅ COMPLETO: TEMPLATE_MASTER_DrDialogue_ANOTADO.py (lido)
2. ✅ VOCÊ ESTÁ AQUI: CHECKLIST_NOVO_SPECIALIST.md
3. ⏭️  PRÓXIMO: DIFF_GUIDE_POR_SPECIALIST.md
4. ⏭️  DEPOIS: validate_specialist.py (rodar validação)
```

---

## ✅ CHECKLIST OBRIGATÓRIA - 60 ITENS

Use esta checklist ANTES de mostrar código novo para o usuário.
Marque cada item com ✅ ou ❌.

---

### SEÇÃO 1: ESTRUTURA DE ARQUIVO (10 itens)

- [ ] **1.1** Arquivo nomeado corretamente: `dr_{nome}.py` (lowercase, snake_case)
- [ ] **1.2** Docstring no topo explicando specialist
- [ ] **1.3** Imports corretos (re, yaml, pathlib, typing, dataclasses, collections, string)
- [ ] **1.4** Nenhum import desnecessário ou ausente
- [ ] **1.5** Dataclasses definidas ANTES da classe principal
- [ ] **1.6** Pelo menos 2 dataclasses (Analysis + Profile/Summary)
- [ ] **1.7** Classe principal nomeada: `Dr{Nome}` (PascalCase)
- [ ] **1.8** Classe de compatibilidade no final: `class DrCharacter{Nome}(Dr{Nome})`
- [ ] **1.9** Nenhum código executável fora de classes/funções
- [ ] **1.10** Comentários [INVARIÁVEL]/[ADAPTAR] presentes (se for template anotado)

---

### SEÇÃO 2: CLASSE PRINCIPAL (__init__) (8 itens)

- [ ] **2.1** `__init__(self, rules_path: str = None)` - assinatura exata
- [ ] **2.2** `self.name` definido (ex: "Script Doctor Structuremon")
- [ ] **2.3** `self.digimon_name` definido
- [ ] **2.4** `self.title` definido
- [ ] **2.5** `self.specialty` definido
- [ ] **2.6** `self.identity` definido
- [ ] **2.7** `self.rules_path` com fallback correto para YAML
- [ ] **2.8** `self.rules = self._load_rules()` chamado

---

### SEÇÃO 3: PATTERNS BILÍNGUES (6 itens)

- [ ] **3.1** Pelo menos 3 patterns/listas definidas em `__init__`
- [ ] **3.2** Cada pattern tem versão INGLÊS (comentário `# English`)
- [ ] **3.3** Cada pattern tem versão PORTUGUÊS (comentário `# Portuguese`)
- [ ] **3.4** Patterns são listas (`[]`) ou sets (`{}`)
- [ ] **3.5** Patterns têm nomes descritivos (não genéricos como `list1`, `list2`)
- [ ] **3.6** Patterns são usados nos métodos de análise

---

### SEÇÃO 4: MÉTODO _load_rules() (3 itens)

- [ ] **4.1** Método existe: `def _load_rules(self) -> Dict:`
- [ ] **4.2** Checa se `self.rules_path.exists()`
- [ ] **4.3** Retorna `{}` (dict vazio) se arquivo não existe

---

### SEÇÃO 5: MÉTODO analyze() PRINCIPAL (12 itens)

- [ ] **5.1** Assinatura EXATA: `def analyze(self, screenplay_text: str) -> Dict[str, Any]:`
- [ ] **5.2** Docstring explica o que faz
- [ ] **5.3** Chama método `_extract_X()` para extrair dados
- [ ] **5.4** Chama múltiplos métodos `_analyze_Y()` para análises
- [ ] **5.5** Chama `_check_{nome}_rules()` para validar regras
- [ ] **5.6** Chama `_calculate_{nome}_score()` para calcular score
- [ ] **5.7** Chama `_generate_diagnosis()` para gerar diagnóstico
- [ ] **5.8** Chama `_generate_recommendations()` para gerar recomendações
- [ ] **5.9** Retorna `Dict[str, Any]`
- [ ] **5.10** Dict retornado tem chave `"specialist"` com metadados
- [ ] **5.11** Dict retornado tem chave `"score"` (float)
- [ ] **5.12** Dict retornado tem chaves obrigatórias (ver checklist detalhada abaixo)

---

### SEÇÃO 6: OUTPUT DO analyze() (10 itens)

Dict retornado DEVE ter TODAS estas chaves:

- [ ] **6.1** `"specialist"` (dict com `name`, `title`, `specialty`)
- [ ] **6.2** `"score"` (float, 5-95)
- [ ] **6.3** `"rule_violations"` (list)
- [ ] **6.4** `"diagnosis"` (str)
- [ ] **6.5** `"recommendations"` (list)
- [ ] **6.6** `"signature"` (str, formato: "Diagnosed by {self.name}™")
- [ ] **6.7** Pelo menos 3 métricas específicas do specialist
- [ ] **6.8** Métricas têm nomes descritivos (não genéricos)
- [ ] **6.9** Valores são serializáveis (int, float, str, list, dict - não objetos custom)
- [ ] **6.10** Nenhuma chave None ou vazia sem razão

---

### SEÇÃO 7: SCORE CALCULATION (8 itens)

- [ ] **7.1** Método existe: `def _calculate_{nome}_score(...) -> float:`
- [ ] **7.2** Base score = **90.0** (NÃO 100, NÃO 85)
- [ ] **7.3** Penalties: critical=-20, high=-15, medium=-8, low=-5 (EXATOS)
- [ ] **7.4** Bonuses graduais (+3 para threshold baixo, +5 para threshold alto)
- [ ] **7.5** Bonuses total MAX +15
- [ ] **7.6** Return tem `max(5.0, min(95.0, score))` (range 5-95)
- [ ] **7.7** Parâmetros incluem `violations: List`
- [ ] **7.8** Itera sobre violations para aplicar penalties

---

### SEÇÃO 8: RULE CHECKING (4 itens)

- [ ] **8.1** Método existe: `def _check_{nome}_rules(...) -> List[Dict]:`
- [ ] **8.2** Itera sobre `self.rules.get("rules", [])`
- [ ] **8.3** Cada violation tem: `rule_id`, `title`, `severity`, `message`, `fix`
- [ ] **8.4** Retorna lista (vazia se sem violations)

---

### SEÇÃO 9: DIAGNOSIS & RECOMMENDATIONS (4 itens)

- [ ] **9.1** Método existe: `def _generate_diagnosis(...) -> str:`
- [ ] **9.2** Método existe: `def _generate_recommendations(...) -> List[str]:`
- [ ] **9.3** Diagnosis inclui score no formato: "{TIPO} {LEVEL} ({score}/100): {summary}"
- [ ] **9.4** Recommendations retorna MAX 5 itens

---

### SEÇÃO 10: ARQUIVO YAML (5 itens)

- [ ] **10.1** Arquivo YAML existe em `specialists/rules/{nome}_rules.yaml`
- [ ] **10.2** YAML tem chave `rules:` (list)
- [ ] **10.3** Cada rule tem: `id`, `title`, `category`, `severity`, `test`, `fail_msg`, `fix`
- [ ] **10.4** Pelo menos 5 regras definidas
- [ ] **10.5** Severities são: critical, high, medium, low (lowercase)

---

## 🔍 VALIDAÇÕES EXTRAS (CRÍTICAS)

### Compatibilidade com DualCoreWrapper

- [ ] **E1** Specialist pode ser instanciado sem parâmetros: `DrDialogue()`
- [ ] **E2** Método `analyze(screenplay_text)` aceita string simples
- [ ] **E3** Método `analyze()` retorna dict (não None, não objeto custom)
- [ ] **E4** Dict retornado é JSON-serializable
- [ ] **E5** Nenhum import de DualCoreWrapper dentro do specialist

### Exportação HTML

- [ ] **E6** Output dict tem chaves que formatted_exporter espera
- [ ] **E7** `rule_violations` segue formato esperado
- [ ] **E8** `signature` está presente

### Tradução

- [ ] **E9** Patterns bilíngues (EN + PT) estão implementados
- [ ] **E10** Diagnosis e recommendations podem ser em PT ou EN (flexível)

---

## ❌ ERROS COMUNS - NÃO FAZER

### ❌ Score Calculation

```python
# ERRADO ❌
score = 100.0  # Base deveria ser 90
score -= 10    # Penalty deveria ser -20 (critical)
return score   # Falta max(5, min(95, score))

# CERTO ✅
score = 90.0
if violation["severity"] == "critical":
    score -= 20
return max(5.0, min(95.0, score))
```

### ❌ Output Format

```python
# ERRADO ❌
return {
    "score": score,
    "problems": violations  # Nome genérico
}

# CERTO ✅
return {
    "specialist": {"name": self.name, ...},
    "score": score,
    "rule_violations": violations,
    "diagnosis": diagnosis,
    "recommendations": recommendations,
    "signature": f"Diagnosed by {self.name}™"
}
```

### ❌ Patterns

```python
# ERRADO ❌
self.markers = ["as you know", "remember when"]  # Só inglês

# CERTO ✅
self.markers = [
    # English
    "as you know", "remember when",
    # Portuguese
    "como você sabe", "lembra quando"
]
```

### ❌ Imports

```python
# ERRADO ❌
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper  # Circular!

# CERTO ✅
import re
import yaml
from pathlib import Path
# ... (apenas stdlib e typing)
```

---

## 🔥🔥🔥 TESTE DE INTEGRAÇÃO DUAL-CORE (OBRIGATÓRIO) 🔥🔥🔥

**CRÍTICO:** Testar APENAS Core 1 isolado NÃO É SUFICIENTE!

### ⚠️ O QUE NÃO FAZER

```python
# ❌ ERRADO - Testa só Core 1 (Python)
from dr_structure import DrStructure
specialist = DrStructure()
result = specialist.analyze(screenplay)  # ~2s - SÓ Python!
print(f"Score: {result['score']}")  # INCOMPLETO!
```

**Problema:** Isso NÃO testa:
- ❌ Theory Search (keywords nos 13 livros)
- ❌ Core 2 (LLM qualitativo)
- ❌ Translation (EN→PT)
- ❌ HTML Export (formatação)

### ✅ O QUE FAZER

**Usar test_integration_complete.py:**

```bash
# ✅ CORRETO - Testa TUDO
python3 /path/to/test_integration_complete.py
```

Este script testa:
1. ✅ Core 1 (Python) - análise objetiva (~2s)
2. ✅ Theory Search - busca nos 13 livros (~1s)
3. ✅ Core 2 (LLM) - análise qualitativa (~4-5 min)
4. ✅ Translation - tradução EN→PT (~30s)
5. ✅ HTML Export - formatação rica (~1s)

**Total esperado: 4-5 minutos**

### 📋 Checklist de Integração

- [ ] **I.1** Executou `test_integration_complete.py`
- [ ] **I.2** Core 1 (Python): PASSED
- [ ] **I.3** Dual-Core (Python + LLM): PASSED (4-5 min)
- [ ] **I.4** HTML Export: PASSED
- [ ] **I.5** Verificou HTML gerado visualmente
- [ ] **I.6** Confirmou teoria relevante foi encontrada
- [ ] **I.7** Tempo total entre 4-5 minutos (não 2 segundos!)

### 🚨 SE O TESTE FALHAR

**Erro comum: DualCoreWrapper missing 'python_specialist'**
- **Causa:** Passar specialist_type em vez de instância
- **Fix:** Ver test_integration_complete.py linha 72-83

**Erro comum: HTML export failed**
- **Causa:** Import path errado ou estrutura de resultado incorreta
- **Fix:** Usar `triple_core.exporters.formatted_exporter`

---

## ✅ QUANDO MARCAR COMO COMPLETO

**SÓ marque checklist como 100% completa quando:**

1. ✅ Todos os 60 itens principais marcados
2. ✅ Todas as 10 validações extras marcadas
3. ✅ Nenhum dos erros comuns presente
4. ✅ Arquivo YAML criado e validado
5. ✅ `validate_specialist.py` passou sem erros
6. ✅ **🔥 TESTE DE INTEGRAÇÃO DUAL-CORE COMPLETO (OBRIGATÓRIO)**

---

## 📚 PRÓXIMOS PASSOS

```
1. ✅ COMPLETO: TEMPLATE_MASTER_DrDialogue_ANOTADO.py
2. ✅ COMPLETO: CHECKLIST_NOVO_SPECIALIST.md (você está aqui)
3. ⏭️  PRÓXIMO: DIFF_GUIDE_POR_SPECIALIST.md
   📍 Localização: /Users/clubproducoes/Digimundo/claude_code/MEMORY/conhecimentos/
4. ⏭️  DEPOIS: validate_specialist.py
```

---

**DIGIMUNDO PRESENTE 🥷**
