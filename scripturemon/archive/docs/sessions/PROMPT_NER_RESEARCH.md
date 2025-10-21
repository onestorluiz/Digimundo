# PROMPT: Pesquisa Implementação NER Anti-Alucinação

## CONTEXTO DO PROJETO

Este é um sistema de análise de roteiros (Scripturemon) que executa 312 análises combinadas:
- 24 especialistas Python (análise estrutural/métrica)
- 13 autores LLM (análise profunda via Ollama + OpenAI)
- Total: 24 × 13 = 312 análises com checkpoint/resume capability

**Problema identificado**: LLMs estavam inventando nomes de personagens com temperatura 0.7 (taxa de alucinação 60-80% segundo pesquisas Stanford 2024 e Nature 2024).

**Soluções já implementadas**:
1. ✅ Temperatura reduzida de 0.7 → 0.2 (commit 1b75dc7)
2. ✅ System prompts com proibições explícitas (commit 1b75dc7)
3. ❌ Tentativa de NER validation FALHOU (variável scope issue)

## PROBLEMA TÉCNICO ENCONTRADO

### Implementação que FALHOU:

```python
def validate_character_hallucinations(screenplay_text: str, analysis_text: str) -> Dict[str, Any]:
    """Valida se a análise inventou personagens"""
    try:
        import spacy
        if not hasattr(validate_character_hallucinations, '_nlp'):
            validate_character_hallucinations._nlp = spacy.load('pt_core_news_lg')

        nlp = validate_character_hallucinations._nlp

        # Extract entities from screenplay
        screenplay_doc = nlp(screenplay_text[:100000])
        real_characters = set()
        for ent in screenplay_doc.ents:
            if ent.label_ == "PER":
                name = ent.text.strip().upper()
                if len(name) > 2:
                    real_characters.add(name)

        # Extract entities from analysis
        analysis_doc = nlp(analysis_text[:50000])
        analysis_characters = set()
        for ent in analysis_doc.ents:
            if ent.label_ == "PER":
                name = ent.text.strip().upper()
                if len(name) > 2:
                    analysis_characters.add(name)

        # Detect invented characters
        invented = analysis_characters - real_characters

        # Filter false positives
        false_positives = {"MCKEE", "FIELD", "TRUBY", "CAMPBELL", "VOGLER", "SEGER",
                          "SNYDER", "EGRI", "WEILAND", "ARISTOTLE", "COWGILL",
                          "PYTHON", "LLM", "SCRIPT", "DOCTOR", "ANÁLISE"}
        invented = invented - false_positives

        return {
            'valid': len(invented) == 0,
            'invented_characters': sorted(list(invented)),
            'confidence': 1.0 / (1.0 + len(invented)),
            'real_characters': real_characters,
            'analysis_characters': analysis_characters
        }
    except Exception as e:
        return {'valid': True, 'invented_characters': [], 'confidence': 0.0, 'error': str(e)}
```

### Problema na Integração:

**Linha ~524 em analyze_all_specialists.py (versão quebrada):**
```python
validation_result = validate_character_hallucinations(
    screenplay_text=screenplay_text,  # ❌ VARIÁVEL NÃO EXISTE NESTE CONTEXTO!
    analysis_text=result.get('llm_insights', '')
)
```

**Sintoma**: Sistema travava/congelava durante testes, nenhum output após 10+ minutos.

## ARQUITETURA ATUAL

### Arquivo Principal: `analyze_all_specialists.py`

**Fluxo de execução:**
1. Load checkpoint (retoma análises anteriores)
2. Loop sobre 24 specialists × 13 authors
3. Para cada combinação:
   - Instancia specialist Python
   - Cria DualCoreWrapper (Python + LLM)
   - Chama `wrapper.analyze(screenplay_path)` ← **passa PATH, não texto!**
   - Salva resultado em `all_analyses.json`
   - Salva checkpoint

**Pontos críticos:**
- O método `wrapper.analyze()` recebe FILE PATH, não texto
- O texto do roteiro é lido DENTRO do wrapper
- No contexto do loop principal, `screenplay_text` não existe
- A validação precisa ser feita DENTRO do DualCoreWrapper ou APÓS resultado retornar

### Arquivo Secundário: `engine/orchestration/dual_core_wrapper.py`

**Estrutura:**
```python
class DualCoreWrapper:
    def __init__(self, python_specialist, specialist_type, llm_model,
                 deep_context=True, use_personalized_prompts=True):
        # ...

    def analyze(self, screenplay_path: str, session_id=None) -> dict:
        # 1. Read screenplay (PDF → text)
        screenplay_text = self._extract_text_from_pdf(screenplay_path)

        # 2. Python specialist analysis
        python_metrics = self.python_specialist.analyze(screenplay_text)

        # 3. Build LLM prompt
        prompt = self._build_prompt(screenplay_text, python_metrics, ...)

        # 4. Call LLM (Ollama or OpenAI)
        llm_insights = self._call_llm(prompt)

        # 5. Return result
        return {
            'llm_insights': llm_insights,
            'python_metrics': python_metrics,
            'quality_score': score,
            # ...
        }
```

**Pontos onde `screenplay_text` EXISTE:**
- ✅ Dentro de `DualCoreWrapper.analyze()` após `_extract_text_from_pdf()`
- ✅ Dentro de `DualCoreWrapper._build_prompt()`
- ✅ Nos métodos internos do wrapper

**Pontos onde `screenplay_text` NÃO EXISTE:**
- ❌ No loop principal de `analyze_all_specialists.py`
- ❌ Após `wrapper.analyze()` retornar (só tem `result` dict)

## QUESTÕES PARA PESQUISA

### 1. ARQUITETURA DE INTEGRAÇÃO

**Opção A: Validação dentro do DualCoreWrapper**
- Adicionar `validate_character_hallucinations()` como método interno
- Chamar após `_call_llm()` mas antes de retornar
- Incluir resultados da validação no dict de retorno

**Vantagens:**
- screenplay_text disponível naturalmente
- Validação automática para TODAS as análises
- Resultado inclui métricas de confiança

**Desvantagens:**
- Aumenta tempo de cada análise (processamento NER)
- Modifica comportamento core do wrapper
- Pode afetar outros usos do wrapper

**Opção B: Validação no loop principal**
- Ler screenplay UMA VEZ no início
- Passar `screenplay_text` junto com `screenplay_path`
- Modificar assinatura de `wrapper.analyze()`

**Vantagens:**
- Lê PDF apenas uma vez por roteiro
- Separação de concerns (validação = camada superior)
- Não modifica lógica interna do wrapper

**Desvantagens:**
- Precisa modificar interface pública (`analyze()`)
- Pode quebrar outros scripts que usam o wrapper
- Duplica leitura de PDF (wrapper lê novamente internamente)

**Opção C: Cache de texto do roteiro**
- Implementar cache global com `screenplay_path` → `text`
- Wrapper usa cache se disponível, senão lê
- Validação acessa cache

**Vantagens:**
- Zero duplicação de leitura
- Não modifica interfaces existentes
- Fácil de implementar/remover

**Desvantagens:**
- Estado global (pode causar bugs)
- Gestão de memória (limpar cache?)
- Complexidade adicional

**❓ PERGUNTA**: Qual opção é mais robusta para long-running batch processes com checkpoint/resume?

### 2. PERFORMANCE E MEMÓRIA

**Considerações:**
- spaCy NER processa ~100k caracteres do screenplay
- spaCy NER processa ~50k caracteres da análise
- Lazy loading do modelo (`pt_core_news_lg`) via hasattr pattern
- 312 análises = muitas chamadas repetidas

**Questões:**
1. ❓ O lazy loading via `hasattr` é thread-safe?
2. ❓ Devemos usar `functools.lru_cache` para entities do screenplay?
3. ❓ Processar screenplay inteiro ou só primeiras N páginas?
4. ❓ Como lidar com screenplays muito longos (>200 páginas)?
5. ❓ NER PT vs EN (roteiros podem ter nomes em inglês)?

### 3. DETECÇÃO DE FALSE POSITIVES

**Problema atual:**
```python
false_positives = {"MCKEE", "FIELD", "TRUBY", "CAMPBELL", "VOGLER", "SEGER",
                  "SNYDER", "EGRI", "WEILAND", "ARISTOTLE", "COWGILL",
                  "PYTHON", "LLM", "SCRIPT", "DOCTOR", "ANÁLISE"}
```

**Limitações:**
- Lista hardcoded (não escalável)
- Pode ter falsos negativos (personagens legítimos não detectados)
- spaCy PT pode confundir nomes comuns ("ANA", "JOÃO") com entidades genéricas

**Questões:**
1. ❓ Como distinguir "JOHN" (personagem inventado) de "John Truby" (citação teórica)?
2. ❓ Usar regex patterns para detectar "Chapter X", "Page Y", "Scene Z"?
3. ❓ Considerar apenas uppercase names (formato roteiro)?
4. ❓ Comparar com lista de nomes brasileiros comuns?
5. ❓ Validar com contexto (frases ao redor da menção)?

### 4. ERROR HANDLING

**Cenários de erro:**
- spaCy modelo não instalado (`pt_core_news_lg`)
- Texto muito longo (OOM)
- Encoding issues (PDF → text)
- NER retorna vazio (screenplay sem personagens detectados?)

**Questões:**
1. ❓ Como falhar gracefully? Retornar `{'valid': True, 'confidence': 0.0}`?
2. ❓ Log warnings vs raise exceptions?
3. ❓ Continuar análises mesmo se validação falhar?
4. ❓ Incluir `validation_skipped` flag no resultado?

### 5. TESTING E VALIDAÇÃO

**Scripts de teste existentes:**
- `test_simple_validation.py` - teste rápido com shallow mode
- `test_anti_hallucination.py` - 3 análises com autores diferentes

**Questões:**
1. ❓ Como criar test cases com ground truth?
2. ❓ Mock de screenplay_text para unit tests?
3. ❓ Benchmark: quanto tempo NER adiciona por análise?
4. ❓ Como testar edge cases (screenplay sem personagens, análise vazia)?

## OBJETIVO DA PESQUISA

**Por favor, investigue e recomende:**

1. **Melhor opção de arquitetura** (A, B, C ou outra) considerando:
   - Robustez para batch processing com checkpoint/resume
   - Mínimo de mudanças na codebase existente
   - Performance (evitar re-processamento)
   - Testabilidade

2. **Melhores práticas para NER validation** em sistemas similares:
   - Como projetos open-source fazem validação de outputs LLM?
   - Alternativas ao spaCy? (Stanza, Flair, transformers?)
   - Técnicas para reduzir false positives

3. **Implementation plan** passo-a-passo:
   - Quais arquivos modificar
   - Onde adicionar código
   - Como testar
   - Como fazer rollback se quebrar

4. **Performance considerations**:
   - Cache strategies
   - Memory management
   - Lazy loading best practices

5. **Error handling patterns**:
   - Graceful degradation
   - Logging estratégico
   - Fallback behaviors

## RECURSOS DISPONÍVEIS

**Arquivos para análise:**
- `/Users/clubproducoes/Digimundo/scripturemon/analyze_all_specialists.py` (loop principal)
- `/Users/clubproducoes/Digimundo/scripturemon/engine/orchestration/dual_core_wrapper.py` (wrapper)
- `/Users/clubproducoes/Digimundo/scripturemon/test_simple_validation.py` (teste funcional)
- `/Users/clubproducoes/Digimundo/scripturemon/test_anti_hallucination.py` (teste 3 autores)

**Git history relevante:**
- `1b75dc7` - Temperature 0.7 → 0.2 + System prompt enhancements
- `0568cf4` - Revert broken NER implementation (current HEAD)

**Dependências instaladas:**
- spacy >= 3.0
- pt_core_news_lg (modelo português)
- PyPDF2 (leitura de PDFs)

## DELIVERABLE ESPERADO

Um documento markdown detalhado com:

1. ✅ **Análise comparativa** das 3 opções de arquitetura (ou proposta de opção D)
2. ✅ **Recomendação clara** de qual opção escolher (com justificativa)
3. ✅ **Código example** da implementação recomendada
4. ✅ **Plano de testes** para validar a solução
5. ✅ **Checklist de implementação** (o que fazer, em qual ordem)
6. ✅ **Riscos e mitigações** (o que pode dar errado, como prevenir)

**Formato sugerido:**
```markdown
# RECOMENDAÇÃO: Implementação NER Anti-Alucinação

## 1. DECISÃO DE ARQUITETURA
[Opção escolhida + justificativa]

## 2. CÓDIGO PROPOSTO
[Exemplos de código para cada arquivo modificado]

## 3. PLANO DE IMPLEMENTAÇÃO
[Passo-a-passo com checklist]

## 4. TESTES E VALIDAÇÃO
[Como testar cada etapa]

## 5. ROLLBACK STRATEGY
[Como reverter se quebrar]

## 6. PERFORMANCE EXPECTATIONS
[Overhead esperado, benchmarks]
```

---

**IMPORTANTE**: Priorize soluções que NÃO quebrem o sistema funcional atual. Estamos em produção com 39/312 análises completas e checkpoint funcionando. Qualquer mudança precisa ser incremental e segura.

**STATUS ATUAL**: Sistema funcional com temperatura 0.2 e system prompts hardened. NER é enhancement, não blocker. Precisamos fazer certo, não fazer rápido.
