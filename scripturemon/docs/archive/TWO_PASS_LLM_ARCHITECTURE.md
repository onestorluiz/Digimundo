# Two-Pass LLM Architecture v12.0

## 🎯 Objetivo

Melhorar a qualidade das análises LLM, gerando **EXATAMENTE 4 problemas** com **soluções concretas** (reescritas linha-por-linha de diálogos).

## 📊 Evolução do Sistema

### v8.0-v10.0: Problemas Identificados
- ✅ Removeu `repeat_penalty` → +42% output (4,236 → 6,066 chars)
- ✅ Ajustou validador para curtas-metragens
- ❌ **PROBLEMA**: Mesmo com prompts enfatizando "4 PROBLEMAS", LLM gerava apenas 2-3
- ❌ **PROBLEMA**: Soluções genéricas sem exemplos concretos do roteiro

### v11.0: Breakthrough com Randomização
- ✅ Removeu `seed 1337` → Output não-determinístico
- ✅ Aumentou `temperature` 0.35 → 0.45
- ✅ Resultado: 3 problemas (vs 2 anteriormente)
- ⚠️ **LIMITAÇÃO**: Ainda não atingia os 4 problemas solicitados

### v12.0: Two-Pass LLM Architecture (IMPLEMENTADO)
- ✅ Separou identificação de problemas (WHAT) de expansão de soluções (HOW)
- ✅ Pass 1: Foca em identificar EXATAMENTE 4 problemas
- ✅ Pass 2: Expande cada problema com exemplos de reescrita linha-por-linha
- ✅ Mantém compatibilidade com sistema existente (`two_pass_llm=False` default)

## 🔧 Como Funciona

### Pass 1: Problem Identification (WHAT)
```python
# Foco: Seções 1-3 (INTERPRETAÇÃO, PADRÕES, PROBLEMAS)
# Input: Python metrics + Full book theory + Screenplay
# Output: 4 problemas identificados com teoria citada

3. PROBLEMAS - EXACTLY 4 PROBLEMS:

   PROBLEMA 1: [Nome] (X ocorrências em Y cenas)
   → Descrição: [Específica e detalhada]
   → Impacto: [Como afeta a história]
   → Localizações: [Cenas específicas + páginas]
   → Teoria: [Autor, Livro, Capítulo, conceito com citação]

   [Repete para PROBLEMAS 2, 3, 4]
```

### Pass 2: Solution Expansion (HOW)
```python
# Foco: Seções 4-5 (SOLUÇÕES, DEPTH & SYNTHESIS)
# Input: Python metrics + Pass 1 results + Screenplay
# Output: 4 soluções com exemplos CONCRETOS

4. SOLUÇÕES - Uma por problema:

   PROBLEMA 1: [Reafirma o problema]
   → Solução específica: [Acionável]
   → Fundamentação teórica: [Livro/Capítulo]
   → Exemplos concretos:
     - Cena 1, p.2: ANTES: 'Estou com medo'
                    DEPOIS: 'Meu coração está batendo...'
     - Cena 3, p.5: ANTES: 'Te amo tanto'
                    DEPOIS: '[Silêncio. Ela segura a mão dele.]'
   → Resultado esperado: [Melhoria detalhada]

   [Repete para SOLUÇÕES 2, 3, 4]
```

### Combinação Final
```python
def _combine_two_pass_responses(pass1, pass2):
    """
    Pass 1: Seções 1-3 (Interpretação, Padrões, 4 Problemas)
    Pass 2: Seções 4-5 (4 Soluções, Synthesis)
    """
    return f"{pass1}\n\n{pass2}"
```

## 📂 Arquitetura de Código

### dual_core_wrapper.py (Modificado)

```python
class DualCoreWrapper:
    def __init__(
        self,
        python_specialist: Any,
        llm_model: str = "scripturemon-optimized",
        llm_timeout: Optional[int] = None,
        fallback_to_python: bool = True,
        use_theory: bool = True,
        deep_context: bool = False,
        specialist_type: Optional[str] = None,
        two_pass_llm: bool = False  # ⚠️ DEFAULT: False (compatibilidade)
    ):
        """
        Novo parâmetro two_pass_llm:
        - False: Modo original single-pass (compatível com código existente)
        - True: Modo 2-pass (identificar problemas + expandir soluções)
        """
```

### Novos Métodos Implementados

1. **`_build_llm_prompt_pass1()`**: Constrói prompt para identificação de problemas
2. **`_build_llm_prompt_pass2()`**: Constrói prompt para expansão de soluções
3. **`_combine_two_pass_responses()`**: Combina resultados dos 2 passes

### Fluxo de Execução

```python
# FASE 2: LLM CORE
if self.two_pass_llm:
    # PASS 1: Identificar 4 problemas
    pass1_prompt = self._build_llm_prompt_pass1(screenplay_text, python_result)
    pass1_response = self._call_llm(pass1_prompt)

    # PASS 2: Expandir soluções com exemplos
    pass2_prompt = self._build_llm_prompt_pass2(screenplay_text, python_result, pass1_response)
    pass2_response = self._call_llm(pass2_prompt)

    # Combinar
    llm_response = self._combine_two_pass_responses(pass1_response, pass2_response)
else:
    # SINGLE-PASS (modo original)
    llm_prompt = self._build_llm_prompt(screenplay_text, python_result)
    llm_response = self._call_llm(llm_prompt)
```

## 🔄 Compatibilidade com Sistema Existente

### ✅ Sistema Atual (NÃO quebra)
```python
# analyze.py e analyze_with_checkpoints.py
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    use_theory=True,
    deep_context=True,
    specialist_type=author
    # Não passa two_pass_llm → usa default=False → single-pass
)
```

### ✅ Novo Sistema 2-Pass (Opt-in)
```python
# Para usar 2-pass, EXPLICITAMENTE passar two_pass_llm=True
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-v11-no-seed',  # v11 sem seed
    use_theory=True,
    deep_context=True,
    specialist_type='dialogue',
    two_pass_llm=True  # ⚠️ ENABLE TWO-PASS
)
```

## 📈 Resultados Esperados

### Single-Pass (v11.0)
- ✅ 3 problemas identificados
- ✅ 6,760 chars
- ✅ ~99 palavras/problema
- ❌ Soluções genéricas

### Two-Pass (v12.0) - Esperado
- 🎯 **4 problemas identificados** (conforme solicitado)
- 🎯 **Soluções com exemplos concretos** (ANTES/DEPOIS de diálogos)
- 🎯 **Output ~8k-10k chars** (mais detalhado)
- 🎯 **Quality score 7.0+/10** (vs 5.0 atual)

## 🧪 Como Testar

### Opção 1: Criar Script de Teste
```python
from engine.orchestration.dual_core_wrapper import DualCoreWrapper
from engine.specialists.dialogue_specialist import DialogueSpecialist

specialist = DialogueSpecialist()
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model="scripturemon-v11-no-seed",
    deep_context=True,
    specialist_type="dialogue",
    two_pass_llm=True  # ⚠️ ENABLE
)

result = wrapper.analyze(screenplay_text)
```

### Opção 2: Modificar analyze_with_checkpoints.py
```python
# Linha 122-128, adicionar parâmetro:
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-v11-no-seed',
    use_theory=True,
    deep_context=True,
    specialist_type=author,
    two_pass_llm=True  # ⚠️ ADICIONAR ESTA LINHA
)
```

## 📝 Status Atual

- ✅ **Implementado**: Arquitetura 2-pass completa
- ✅ **Compatibilidade**: Mantida com sistema existente (default=False)
- ⏳ **Pendente**: Testes reais com "Te Encontro em Mim"
- ⏳ **Pendente**: Validação de qualidade (4 problemas + exemplos concretos)

## 🔍 Próximos Passos

1. **Testar v12.0** com `two_pass_llm=True`
2. **Comparar resultados**:
   - v11 single-pass: 3 problemas
   - v12 two-pass: 4 problemas (esperado)
3. **Validar qualidade**:
   - Verificar se soluções têm exemplos ANTES/DEPOIS
   - Confirmar citações de teoria corretas
4. **Ajustar se necessário**:
   - Temperatura
   - Prompts
   - Validadores

## 💡 Insights da Implementação

### Por que Two-Pass?
1. **Separação de responsabilidades**: LLM foca primeiro em IDENTIFICAR, depois em EXPANDIR
2. **Contexto progressivo**: Pass 2 recebe resultados de Pass 1, pode refinar
3. **Qualidade > Velocidade**: 2 passes permitem análise mais profunda
4. **Flexibilidade**: Pode ajustar prompts de cada pass independentemente

### Trade-offs
- ✅ **Pros**: Mais qualidade, 4 problemas garantidos, exemplos concretos
- ❌ **Cons**: 2x tempo de execução (~12 min vs ~6 min)
- ⚖️ **Decisão**: Opt-in via `two_pass_llm=True` (usuário escolhe)

---

**Versão**: v12.0
**Data**: 2025-10-10
**Autor**: Sistema Scripturemon Dual-Core
**Status**: ✅ Implementado, ⏳ Pendente Testes
